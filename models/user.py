import enum
import typing as t

import sqlalchemy as sa
from fastapi_users.db import SQLAlchemyBaseUserTable
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.db import Base

if t.TYPE_CHECKING:
    from models.telegram import TelegramResponse


class UserRoleEnum(enum.Enum):
    user = 'user'
    manager = 'manager'
    admin = 'admin'


class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(
        sa.String(length=320), unique=True, index=True, nullable=False
    )
    hashed_password: Mapped[str] = mapped_column(
        sa.String(length=1024), nullable=False
    )
    is_active: Mapped[bool] = mapped_column(sa.Boolean, default=True, nullable=False)
    is_verified: Mapped[bool] = mapped_column(
        sa.Boolean, default=False, nullable=False
    )
    role: Mapped[enum.Enum] = mapped_column(sa.Enum(UserRoleEnum), default=UserRoleEnum.user)
    telegram_responses: Mapped[list['TelegramResponse']] = relationship(back_populates="user")
    manager: Mapped[t.Optional['Manager']] = relationship()


class Manager(Base):
    __tablename__ = 'user_manager'

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(sa.ForeignKey('user.id'), unique=True)
    user: Mapped['User'] = relationship()


class UserManagerAssociation(Base):
    __tablename__ = 'users_user_managers'

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(sa.ForeignKey('user.id'))
    user: Mapped['User'] = relationship()
    manager_id: Mapped[int] = mapped_column(sa.ForeignKey('user_manager.id'))
    manager: Mapped['Manager'] = relationship()
