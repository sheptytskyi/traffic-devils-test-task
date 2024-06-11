from fastapi_users import BaseUserManager, models
from fastapi_users.db import BaseUserDatabase
from models.user import User


class CustomBaseUserDatabase(BaseUserDatabase[models.UP, models.ID]):
    async def set_users_to_manager(self, users_id: list[int], manager_id: int) -> None:
        """Set users to manager"""
        raise NotImplementedError()

    async def create_manager(self, user_id: int) -> None:
        """Create manager"""
        raise NotImplementedError()


class CustomBaseUserManager(BaseUserManager[User, int]):
    user_db: CustomBaseUserDatabase

    async def set_users_to_manager(self, users_id: list[int], manager_id: int) -> None:
        return await self.user_db.set_users_to_manager(
            users_id=users_id,
            manager_id=manager_id
        )

    async def create_manager(self, user_id: int) -> None:
        return await self.user_db.create_manager(user_id=user_id)
