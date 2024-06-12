import typing as t
from logging import getLogger

import sqlalchemy as sa
from fastapi import Depends, Request, HTTPException, status
from fastapi_users import FastAPIUsers, IntegerIDMixin
from fastapi_users.authentication import (
    AuthenticationBackend,
    BearerTransport,
    JWTStrategy,
)
from fastapi_users.db import SQLAlchemyUserDatabase
from sqlalchemy.future import select

from models.user import User, Manager, UserManagerAssociation
from database.db import AsyncSession, get_async_session
from configuration.config import config
from services.base_user import CustomBaseUserManager

logger = getLogger(__name__)


class CustomSQLAlchemyUserDatabase(SQLAlchemyUserDatabase):
    async def set_users_to_manager(self, users_id: list[int], manager_id: int) -> None:
        stmt = (
            sa.delete(UserManagerAssociation)
            .filter(UserManagerAssociation.manager_id == manager_id)
        )
        await self.session.execute(stmt)
        self.session.add_all([
            UserManagerAssociation(user_id=user_id, manager_id=manager_id)
            for user_id in users_id
        ])
        await self.session.flush()
        await self.session.commit()

    async def create_manager(self, user_id: int) -> None:
        instance = Manager(user_id=user_id)
        self.session.add(instance=instance)
        await self.session.flush()
        await self.session.commit()


class UserManager(IntegerIDMixin, CustomBaseUserManager):
    reset_password_token_secret = config.jwt_secret
    verification_token_secret = config.jwt_secret

    async def on_after_register(
        self, user: User, request: Request | None = None
    ) -> None:
        logger.info(f"User {user.id} has registered.")

    async def on_after_forgot_password(
        self, user: User, token: str, request: Request | None = None
    ) -> None:
        logger.info(f"User {user.id} has forgot their password. Reset token: {token}")

    async def on_after_request_verify(
        self, user: User, token: str, request: Request | None = None
    ) -> None:
        logger.info(f"Verification requested for user {user.id}. Verification token: {token}")

    async def set_users_to_manager(
        self, users_id: list[int], manager_id: int
    ) -> None:
        return await self.user_db.set_users_to_manager(users_id=users_id, manager_id=manager_id)

    async def create_manager(self, user_id: int) -> None:
        return await self.user_db.create_manager(user_id=user_id)


async def get_user_db(
    session: AsyncSession = Depends(get_async_session)
) -> t.AsyncGenerator[CustomSQLAlchemyUserDatabase, None]:
    yield CustomSQLAlchemyUserDatabase(session, User)


async def get_user_manager(
    user_db: SQLAlchemyUserDatabase = Depends(get_user_db)
) -> t.AsyncGenerator[UserManager, None]:
    yield UserManager(user_db)


bearer_transport = BearerTransport(tokenUrl="auth/jwt/login")


def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=config.jwt_secret, lifetime_seconds=config.jwt_lifetime)


auth_backend = AuthenticationBackend(
    name="jwt",
    transport=bearer_transport,
    get_strategy=get_jwt_strategy,
)

fastapi_users = FastAPIUsers[User, int](get_user_manager, [auth_backend])

current_active_user = fastapi_users.current_user(active=True)


async def get_current_active_manager(
    user: User = Depends(current_active_user),
    session: AsyncSession = Depends(get_async_session)
) -> Manager:
    query = select(Manager).filter(Manager.user_id == user.id)
    result = await session.execute(query)
    if manager := result.scalar_one_or_none():
        return manager
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail='User is not a manager'
    )
