from logging import getLogger

from fastapi import APIRouter, Depends, Body, status, HTTPException
from fastapi.responses import JSONResponse

from schemas.telegram import TelegramResponse
from models.user import User
from schemas.telegram import TelegramMessage, TelegramMessageWithUser
from services.user import current_active_user
from services.telegram import TelegramManager, get_telegram_manager

logger = getLogger(__name__)


router = APIRouter(
    prefix='',
    tags=['telegram']
)


@router.post('/send-message')
async def send_message(
    user: User = Depends(current_active_user),
    message_data: TelegramMessage = Body(...),
    telegram_manager: TelegramManager = Depends(get_telegram_manager)
) -> JSONResponse:
    try:
        message_data_with_user = TelegramMessageWithUser(
            **message_data.model_dump(),
            user_id=user.id
        )
        await telegram_manager.send_message_by_bot(message_data=message_data_with_user)
        return JSONResponse(
            content={
                'user': user.email,
                'message_data': message_data.message
            },
            status_code=status.HTTP_200_OK
        )
    except Exception as e:
        logger.error(str(e))
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        ) from e


@router.get('/get-all-records', response_model=list[TelegramResponse])
async def get_all_records(
    user: User = Depends(current_active_user),
    telegram_manager: TelegramManager = Depends(get_telegram_manager)
):
    try:
        return await telegram_manager.get_all_records(user=user)
    except Exception as e:
        logger.error(str(e))
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        ) from e
