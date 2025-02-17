from typing import Generic, TypeVar, Optional
from pydantic import BaseModel

T = TypeVar('T')

class ResponseSchema(BaseModel, Generic[T]):
    status_message: str
    message: str
    data: Optional[T]
    status_code: int

    class Config:
        from_attributes = True