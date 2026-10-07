"""
models.py - database TABLES (SQLAlchemy).

One class = one table. One attribute = one column.
Do not confuse with schemas.py (Pydantic) which describes API JSON.
"""
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from database import Base


# id: Mapped[int] -> creates column in db with data type int
# mapped_column(primary_key=True)  -> gives extra information that what extra column configuration you want
class Employee(Base):
    __tablename__ = "employees"


    id: Mapped[int] = mapped_column(primary_key=True)                  # auto-numbered
    name: Mapped[str] = mapped_column(String(50))
    email: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    department: Mapped[str] = mapped_column(String(30))
    salary: Mapped[float]
    is_active: Mapped[bool] = mapped_column(default=True)
