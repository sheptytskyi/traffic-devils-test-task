from pydantic import BaseModel, EmailStr, ConfigDict
from fastapi_users import schemas, models

from models.user import UserRoleEnum


class CreateUpdateDictModel(BaseModel):
    def create_update_dict(self):
        return schemas.model_dump(
            self,
            exclude_unset=True,
            exclude={
                "id",
                "is_active",
                "is_verified",
                "oauth_accounts",
            },
        )

    def create_update_dict_superuser(self):
        return schemas.model_dump(self, exclude_unset=True, exclude={"id"})


class BaseUser(CreateUpdateDictModel):
    id: models.ID
    email: EmailStr
    is_active: bool = True
    is_verified: bool = False
    role: UserRoleEnum = UserRoleEnum.user

    model_config = ConfigDict(from_attributes=True)


class UserRead(BaseUser):
    pass


class UserCreate(CreateUpdateDictModel):
    email: EmailStr
    password: str


class UserUpdate(CreateUpdateDictModel):
    email: EmailStr
    password: str
    is_active: bool
    is_verified: bool
    role: UserRoleEnum


class SetUserToManager(BaseModel):
    users_id: list[int]
