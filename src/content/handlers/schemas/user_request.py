from pydantic import BaseModel


class UserRequest(BaseModel):
    tg_id: int
    article: int
