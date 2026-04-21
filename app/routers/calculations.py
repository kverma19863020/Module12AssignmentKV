from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.calculation import Calculation
from app.models.user import User
from app.schemas.calculation import (
    CalculationCreate,
    CalculationRead,
    CalculationUpdate,
)

router = APIRouter(prefix="/calculations", tags=["Calculations"])


@router.get("/", response_model=List[CalculationRead])
def browse(user_id: Optional[int] = None, db: Session = Depends(get_db)):
    query = db.query(Calculation)
    if user_id:
        query = query.filter(Calculation.user_id == user_id)
    return query.all()


@router.get("/{calc_id}", response_model=CalculationRead)
def read(calc_id: int, db: Session = Depends(get_db)):
    calc = db.query(Calculation).filter(Calculation.id == calc_id).first()
    if not calc:
        raise HTTPException(status_code=404, detail="Calculation not found")
    return calc


@router.post(
    "/",
    response_model=CalculationRead,
    status_code=status.HTTP_201_CREATED
)
def add(request: CalculationCreate, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == request.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    try:
        result = Calculation.compute(request.type, request.inputs)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    calc = Calculation(
        user_id=request.user_id,
        type=request.type,
        inputs=request.inputs,
        result=result,
    )
    db.add(calc)
    db.commit()
    db.refresh(calc)
    return calc


@router.put("/{calc_id}", response_model=CalculationRead)
def edit(
    calc_id: int,
    request: CalculationUpdate,
    db: Session = Depends(get_db)
):
    calc = db.query(Calculation).filter(Calculation.id == calc_id).first()
    if not calc:
        raise HTTPException(status_code=404, detail="Calculation not found")
    if request.type is not None:
        calc.type = request.type
    if request.inputs is not None:
        calc.inputs = request.inputs
    try:
        calc.result = Calculation.compute(calc.type, calc.inputs)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    db.commit()
    db.refresh(calc)
    return calc


@router.delete("/{calc_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete(calc_id: int, db: Session = Depends(get_db)):
    calc = db.query(Calculation).filter(Calculation.id == calc_id).first()
    if not calc:
        raise HTTPException(status_code=404, detail="Calculation not found")
    db.delete(calc)
    db.commit()
