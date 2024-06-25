from typing import Optional

from pydantic import BaseModel, Field, ConfigDict


class ChangePassword(BaseModel):
    model_config = ConfigDict(extra='forbid')
    login: Optional[str] = Field(None, description='User login')
    token: str
    old_password: Optional[str] = Field(None, serialization_alias='oldPassword')
    new_password: Optional[str] = Field(None, serialization_alias='newPassword')
