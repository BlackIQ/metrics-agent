# Pydantic
from pydantic import BaseModel, ConfigDict


# BaseSchema
class BaseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
