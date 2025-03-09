from pydantic import BaseModel, Field
from typing import Optional


class Task(BaseModel):
    id: Optional[int] = Field(default=None, example=1)
    title: str = Field(..., example="Купить продукты")
    description: Optional[str] = Field(default="", example="Молоко, хлеб, яйца")
    status: str = Field(default="pending", example="pending")
