from fastapi import APIRouter, status, Depends, Body, HTTPException
from fastapi.responses import JSONResponse

from models.user import Manager, User
from services.user import get_current_active_manager, UserManager, get_user_manager, current_active_user
from schemas.user import SetUserToManager

router = APIRouter(
    prefix='',
    tags=['users']
)


@router.post('/create-manager')
async def create_manager(
    user: User = Depends(current_active_user),
    user_manager: UserManager = Depends(get_user_manager),
) -> JSONResponse:
    try:
        await user_manager.create_manager(user_id=user.id)
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={'message': f'Manager for user: {user.email} successfully created'}
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        ) from e


@router.post('/set_users_to_manager')
async def set_users_to_manager(
    users_id: SetUserToManager = Body(...),
    user_manager: UserManager = Depends(get_user_manager),
    manager: Manager = Depends(get_current_active_manager),
) -> JSONResponse:
    try:
        await user_manager.set_users_to_manager(
            users_id=users_id.users_id,
            manager_id=manager.id
        )
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={'message': f'Users with ids: {users_id} now are managing by manager with id {manager.id}'}
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        ) from e
