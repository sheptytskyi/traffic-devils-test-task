from fastapi import FastAPI
from configuration.logger import logger
from configuration.config import config
from services.user import fastapi_users, auth_backend
from schemas.user import UserCreate, UserUpdate, UserRead
from routers.telegram import router as telegram_router
from routers.user import router as user_router


app = FastAPI(
    debug=config.debug,
    title=config.application_name,
    version=config.api_version,
    description=config.application_description
)

app.include_router(
    fastapi_users.get_auth_router(auth_backend), prefix="/auth/jwt", tags=["auth"]
)
app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_reset_password_router(),
    prefix="/auth",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_verify_router(UserRead),
    prefix="/auth",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix="/users",
    tags=["users"],
)
app.include_router(
    user_router,
    prefix='/users',
    tags=['users']
)
app.include_router(
    telegram_router,
    prefix='/telegram',
    tags=['telegram']
)

# @app.on_event('startup')
# async def startup():
#     logger.debug('Application started')
