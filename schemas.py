"""
schemas.py - API data shapes (Pydantic, Module 02).

from_attributes=True lets Pydantic read a SQLAlchemy object
(employee.name) instead of only dictionaries (employee["name"]).
"""
from pydantic import BaseModel, ConfigDict, Field
from typing import Optional

class EmployeeCreate(BaseModel):
    name: str = Field(min_length=2, max_length=50)
    email: str = Field(pattern=r"^[\w.+-]+@[\w-]+\.[\w.]+$")
    department: str = Field(min_length=2, max_length=30)
    salary: float = Field(gt=0)


class EmployeeUpdate(BaseModel):
    name: Optional[str] = Field(default=None, min_length=2, max_length=50)
    department: Optional[str] = Field(default=None, min_length=2, max_length=30)
    salary: Optional[float] = Field(default=None, gt=0)
    is_active: Optional[bool] = None


class EmployeeResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    email: str
    department: str
    salary: float
    is_active: bool
