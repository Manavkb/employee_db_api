"""
===============================================================================
 FASTAPI CORPORATE TRAINING
 Module 05 - Databases with SQLAlchemy (CRUD)
 Project : Enterprise Employee Management API
===============================================================================

FILES
    database.py  -> connection, session, get_db()
    models.py    -> tables  (SQLAlchemy)
    schemas.py   -> JSON    (Pydantic)
    crud.py      -> database operations
    main.py      -> endpoints (this file)

RUN (from this folder)
    pip install fastapi uvicorn sqlalchemy
    uvicorn main:app --reload
    open http://127.0.0.1:8000/docs

Data is saved in employees.db - it SURVIVES restarts (unlike Modules 01-04).
Delete the file to start fresh.
===============================================================================
"""
from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI, HTTPException, Query, Response, status
from sqlalchemy.orm import Session
from typing import Optional

import crud
import models
import schemas
from database import Base, SessionLocal, engine, get_db



@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)        # create tables if they don't exist
    with SessionLocal() as db:                   # add sample data the first time only
        if crud.get_employees(db, limit=1) == []:
            for e in [
                {"name": "Asha Rao", "email": "asha@novatech.com", "department": "Engineering", "salary": 1800000},
                {"name": "Priya Nair", "email": "priya@novatech.com", "department": "HR", "salary": 1500000},
                {"name": "Rahul Mehta", "email": "rahul@novatech.com", "department": "Engineering", "salary": 2100000},
            ]:
                crud.create_employee(db, schemas.EmployeeCreate(**e))
    print("Database ready: employees.db")
    yield


app = FastAPI(title="Enterprise Employee Management API",
              description="Module 05 - Databases with SQLAlchemy", version="5.0.0", lifespan=lifespan)


# Module 04 pattern: load-or-404 as a dependency - now using the database
def get_employee_or_404(employee_id: int, db: Session = Depends(get_db)) -> models.Employee:
    employee = crud.get_employee(db, employee_id)
    if employee is None:
        raise HTTPException(status_code=404, detail=f"Employee {employee_id} not found")
    return employee


# ---------------- CREATE ----------------
@app.post("/employees", response_model=schemas.EmployeeResponse,
          status_code=status.HTTP_201_CREATED, tags=["Employees"])
def create_employee(payload: schemas.EmployeeCreate, db: Session = Depends(get_db)):
    if crud.get_employee_by_email(db, payload.email):
        raise HTTPException(status_code=409, detail="Email already registered")
    return crud.create_employee(db, payload)


# ---------------- READ (list) ----------------
@app.get("/employees",
         response_model=list[schemas.EmployeeResponse],
         tags=["Employees"])
def list_employees(skip: int = Query(0, ge=0),
                   limit: int = Query(10, ge=1, le=100),
                   department: Optional[str] = None,
                   db: Session = Depends(get_db)):
    return crud.get_employees(db,
                              skip=skip,
                              limit=limit,
                              department=department)


# ---------------- READ (one) ----------------
@app.get("/employees/{employee_id}", response_model=schemas.EmployeeResponse, tags=["Employees"])
def read_employee(employee: models.Employee = Depends(get_employee_or_404)):
    return employee


# ---------------- UPDATE ----------------
@app.patch("/employees/{employee_id}", response_model=schemas.EmployeeResponse, tags=["Employees"])
def update_employee(payload: schemas.EmployeeUpdate,
                    employee: models.Employee = Depends(get_employee_or_404),
                    db: Session = Depends(get_db)):
    return crud.update_employee(db, employee, payload)


# ---------------- DELETE ----------------
@app.delete("/employees/{employee_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Employees"])
def delete_employee(employee: models.Employee = Depends(get_employee_or_404),
                    db: Session = Depends(get_db)):
    crud.delete_employee(db, employee)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

if __name__ == '__main__':
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)