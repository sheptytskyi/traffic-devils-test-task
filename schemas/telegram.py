import datetime

from pydantic import BaseModel, ConfigDict

from schemas.user import UserRead


class TelegramMessage(BaseModel):
    bottoken: str
    chatid: str
    message: str


class TelegramMessageWithUser(TelegramMessage):
    user_id: int


class TelegramResponseFrom(BaseModel):
    id: int
    is_bot: bool = True
    first_name: str | None = None
    last_name: str | None = None
    username: str | None = None


class TelegramResponseChat(BaseModel):
    id: int
    first_name: str | None = None
    last_name: str | None = None
    username: str | None = None
    type: str


class TelegramResponseResult(BaseModel):
    message_id: int
    from_: TelegramResponseFrom
    chat: TelegramResponseChat
    date: int
    text: str


class TelegramResponseSuccess(BaseModel):
    ok: bool = True
    result: TelegramResponseResult
    user_id: int


class TelegramResponseError(BaseModel):
    ok: bool = False
    error_code: int = 400
    description: str


class TelegramResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    message_id: int
    from_id: int
    from_is_bot: bool
    from_first_name: str | None
    from_last_name: str | None
    from_username: str | None
    chat_id: int
    chat_first_name: str | None
    chat_last_name: str | None
    chat_username: str | None
    chat_type: str
    date: datetime.datetime
    text: str
    user: UserRead
