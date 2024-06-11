import datetime
import typing as t
from logging import getLogger

from fastapi import Depends
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload

from schemas.telegram import TelegramMessageWithUser, TelegramResponseSuccess, TelegramResponseError, \
    TelegramResponse as TelegramResponseSchema
from database.db import get_async_session
from models.telegram import TelegramResponse
from models.user import User, UserRoleEnum, UserManagerAssociation, Manager


logger = getLogger(__name__)


class TelegramManager:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.telegram_send_message_url = 'https://api.telegram.org/bot%s/sendMessage'

    async def __store_telegram_response(
        self,
        telegram_response: TelegramResponseSuccess
    ) -> None:
        # noinspection PyArgumentList
        model = TelegramResponse(
            message_id=telegram_response.result.message_id,
            from_id=telegram_response.result.from_.id,
            from_is_bot=telegram_response.result.from_.is_bot,
            from_first_name=telegram_response.result.from_.first_name,
            from_last_name=telegram_response.result.from_.last_name,
            from_username=telegram_response.result.from_.username,
            chat_id=telegram_response.result.chat.id,
            chat_first_name=telegram_response.result.chat.first_name,
            chat_last_name=telegram_response.result.chat.last_name,
            chat_username=telegram_response.result.chat.username,
            chat_type=telegram_response.result.chat.type,
            date=datetime.datetime.fromtimestamp(telegram_response.result.date),
            text=telegram_response.result.text,
            user_id=telegram_response.user_id
        )
        self.session.add(model)
        await self.session.flush()
        await self.session.commit()

    async def send_message_by_bot(
        self,
        message_data: TelegramMessageWithUser
    ) -> None:
        async with AsyncClient() as client:
            response = await client.post(
                url=self.telegram_send_message_url % message_data.bottoken,
                json={'chat_id': message_data.chatid, 'text': message_data.message}
            )
            response_data = response.json()
            if response.status_code == 200:
                response_data['result']['from_'] = response_data['result'].pop('from')
                telegram_response = TelegramResponseSuccess(
                    **response_data,
                    user_id=message_data.user_id
                )
                await self.__store_telegram_response(telegram_response=telegram_response)
            else:
                response_data = TelegramResponseError(**response_data)
                logger.error(response_data.description)
                raise Exception(response_data.description)

    @staticmethod
    def __serializer(records: t.Sequence) -> list[TelegramResponseSchema]:
        return [
            TelegramResponseSchema.from_orm(record)
            for record in records
        ]

    async def __all_records_for_admin(self) -> list[TelegramResponseSchema]:
        query = (
            select(TelegramResponse)
            .options(
                joinedload(TelegramResponse.user)
            )
        )
        result = await self.session.execute(query)
        telegram_responses = result.scalars().all()
        return self.__serializer(telegram_responses)

    async def __all_records_for_manager(self, user: User) -> list[TelegramResponseSchema]:
        user_ids = (
            select(
                UserManagerAssociation.user_id
            )
            .filter(Manager.user_id == user.id)
            .subquery()
        )
        query = (
            select(TelegramResponse)
            .where(TelegramResponse.user_id.in_(user_ids))
            .options(
                joinedload(TelegramResponse.user)
            )
        )
        result = await self.session.execute(query)
        telegram_responses = result.scalars().all()
        return self.__serializer(telegram_responses)

    async def __all_records_for_user(self, user: User) -> list[TelegramResponseSchema]:
        query = (
            select(TelegramResponse)
            .filter(TelegramResponse.user_id == user.id)
            .options(
                joinedload(TelegramResponse.user)
            )
        )
        result = await self.session.execute(query)
        telegram_responses = result.scalars().all()
        return self.__serializer(telegram_responses)

    async def get_all_records(self, user: User) -> list[TelegramResponseSchema]:
        match user.role:
            case UserRoleEnum.user:
                return await self.__all_records_for_user(user=user)
            case UserRoleEnum.manager:
                return await self.__all_records_for_manager(user=user)
            case UserRoleEnum.admin:
                return await self.__all_records_for_admin()


async def get_telegram_manager(
    session: AsyncSession = Depends(get_async_session)
) -> t.AsyncGenerator[TelegramManager, None]:
    yield TelegramManager(session=session)
