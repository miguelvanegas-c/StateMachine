# app/schemas/response.py
from pydantic import BaseModel, Field
from typing import Generic, TypeVar, Optional, Any

T = TypeVar('T')

# app/schemas/response.py
from pydantic import BaseModel, Field
from typing import Generic, TypeVar, Optional, Any, List

T = TypeVar('T')

class APIResponse(BaseModel, Generic[T]):
    success: bool = Field(default=True)
    message: str = Field(default="Operation successful")
    data: Optional[T] = None
    status_code: int = Field(default=200)

class ErrorResponse(APIResponse[Any]):
    success: bool = Field(default=False)
    details: Optional[Any] = Field(None, description="Mensaje técnico para el desarrollador")

    class Config:
        pass