from bson import ObjectId
from pydantic import BaseModel, Field

from core.models.objects import PyObjectId
from core.schemas.sheets import Sheet


class ModelMeta(BaseModel):
    name: str
    # todo what else?


class Model(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    meta: ModelMeta
    data: list[Sheet]

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

