from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class ChangeEmail(BaseModel):
    model_config = ConfigDict(extra='forbid')
    login: Optional[str] = Field(..., description='Логин')
    password: Optional[str] = Field(..., description='Email')
    email: Optional[str] = Field(..., description='Пароль')
