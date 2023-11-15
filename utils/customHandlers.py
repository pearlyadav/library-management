import typing, json, datetime
from bson import ObjectId
from fastapi import Response
from pydantic.json_schema import JsonSchemaValue
from pydantic_core import core_schema
from pydantic import GetCoreSchemaHandler, GetJsonSchemaHandler

def default(obj):
    if isinstance(obj, ObjectId) or isinstance(obj, datetime.datetime):
        return str(obj)
    raise TypeError

class customResponse(Response):
    media_type = 'application/json'

    def __init__(self, content: typing.Any = None):
        super().__init__(content, 200)

    def render(self, content) -> bytes:
        return (json.dumps(content, default=default)).encode(Response.charset)
    
class customObjectId(ObjectId):    
    @classmethod
    def validate_object_id(cls, value, handler) -> ObjectId:
        if isinstance(value, ObjectId):
            return value
        
        s = handler(value)
        if ObjectId.is_valid(s):
            return ObjectId(value)
        else:
            raise ValueError(f"Invalid Object ID - {value}")
    
    @classmethod
    def __get_pydantic_core_schema__(cls, source_type: typing.Any, handler: GetCoreSchemaHandler) -> core_schema.CoreSchema:
        return core_schema.no_info_wrap_validator_function(
            cls.validate_object_id,  # Validator function
            core_schema.str_schema(),
            serialization=core_schema.to_string_ser_schema()
        )

    @classmethod
    def __get_pydantic_json_schema__(cls, _core_schema: core_schema.CoreSchema, handler: GetJsonSchemaHandler) -> JsonSchemaValue:
        return handler(core_schema.str_schema())
