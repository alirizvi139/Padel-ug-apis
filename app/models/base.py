from datetime import datetime
from typing import Optional, Annotated
from pydantic import BaseModel, Field, GetJsonSchemaHandler
from pydantic.json_schema import JsonSchemaValue
from bson import ObjectId


class PyObjectId(ObjectId):
    @classmethod
    def __get_pydantic_core_schema__(cls, source_type, handler):
        from pydantic_core import core_schema
        return core_schema.json_schema(core_schema.str_schema())
    
    @classmethod
    def __get_pydantic_json_schema__(
        cls, _core_schema, _handler: GetJsonSchemaHandler
    ) -> JsonSchemaValue:
        return {"type": "string"}


class BaseDocument(BaseModel):
    id: Optional[str] = Field(default=None, alias="_id")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True 