from bson import ObjectId
from pydantic import BaseModel, Field

from core.objects import PyObjectId


class User(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    username: str
    first_name: str | None = None
    last_name: str | None = None
    disabled: bool | None = None

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "_id": "62bb11835529faba0704639d",
                "username": "johndoe@example.com",
                "first_name": "John",
                "last_name": "Doe",
                "disabled": False,
            }
        }


class UserInfo(BaseModel):
    class WorkspaceInfo(BaseModel):
        id: str = Field(alias="_id")
        name: str

    class ModelInfo(BaseModel):
        id: str = Field(alias="_id")
        name: str

    id: str = Field(alias="_id")
    username: str
    first_name: str | None = None
    last_name: str | None = None
    workspaces: list[WorkspaceInfo]
    models: list[ModelInfo]


class RegisterUser(BaseModel):
    username: str
    first_name: str
    last_name: str
    workspace_id: PyObjectId
    password: str

    class Config(User.Config):
        schema_extra = {
            "example": {
                "username": "jdoe@example.com",
                "first_name": "John",
                "last_name": "Doe",
                "workspace_id": "62bc5706a40e85213c27ce28",
                "password": "secret",
            }
        }


class UserInDB(User):
    hashed_password: str
    otp_secret: str | None
    otp_validated: bool = False
