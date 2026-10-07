"""
crud.py - Create, Read, Update, Delete.

All database work lives here. Plain Python: no FastAPI imports.
Every function receives the session `db` as its first argument.
"""
from sqlalchemy import select
from sqlalchemy.orm import Session
from typing import Optional

import models
import schemas


# ---------- READ ----------
def get_employee(db: Session, employee_id: int) -> Optional[models.Employee]:
    return db.get(models.Employee, employee_id)


def get_employee_by_email(db: Session, email: str) -> Optional[models.Employee]:
    return db.scalars(select(models.Employee).where(models.Employee.email == email)).first()


def get_employees(db: Session,
                  skip: int = 0,
                  limit: int = 10,
                  department: Optional[str] = None) -> list[models.Employee]:

    query = select(models.Employee) # SELECT * FROM employees
    if department:
        # SELECT * FROM employees WHERE department = 'Engineering'
        query = query.where(models.Employee.department == department)

    # SELECT *
    # FROM employees
    # WHERE department = 'Engineering'
    # ORDER BY id
    # OFFSET 10
    # LIMIT 5;

    query = query.order_by(models.Employee.id).offset(skip).limit(limit)
    return list(db.scalars(query).all())


# ---------- CREATE ----------
def create_employee(db: Session, data: schemas.EmployeeCreate) -> models.Employee:
    employee = models.Employee(**data.model_dump())   # 1. build the object
    db.add(employee)                                  # 2. stage it
    db.commit()                                       # 3. save permanently
    db.refresh(employee)                              # 4. reload (gets the new id)
    return employee


# ---------- UPDATE ----------
def update_employee(db: Session, employee: models.Employee,
                    data: schemas.EmployeeUpdate) -> models.Employee:
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(employee, field, value)               # change only sent fields
    db.commit()
    db.refresh(employee)
    return employee


# ---------- DELETE ----------
def delete_employee(db: Session, employee: models.Employee) -> None:
    db.delete(employee)
    db.commit()
