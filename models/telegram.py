from typing import TYPE_CHECKING
import datetime

import pytz
import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.db import Base
from configuration.config import config

if TYPE_CHECKING:
    from models.user import User


class TelegramResponse(Base):
    __tablename__ = 'telegram_response'

    id: Mapped[int] = mapped_column(primary_key=True)
    message_id: Mapped[int]
    from_id: Mapped[int] = mapped_column(sa.BigInteger)
    from_is_bot: Mapped[bool]
    from_first_name: Mapped[str | None]
    from_last_name: Mapped[str | None]
    from_username: Mapped[str | None]
    chat_id: Mapped[int] = mapped_column(sa.BigInteger)
    chat_first_name: Mapped[str | None]
    chat_last_name: Mapped[str | None]
    chat_username: Mapped[str | None]
    chat_type: Mapped[str]
    date: Mapped[datetime.datetime] = mapped_column(
        sa.DateTime(timezone=True),
        default=datetime.datetime.now(tz=pytz.timezone(config.timezone))
    )
    text: Mapped[str]
    user_id: Mapped[int] = mapped_column(sa.ForeignKey('user.id'))
    user: Mapped['User'] = relationship(back_populates='telegram_responses')
