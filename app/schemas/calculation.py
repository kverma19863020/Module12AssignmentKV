from datetime import datetime
from typing import Any, Dict, Optional
from pydantic import BaseModel


class CalculationCreate(BaseModel):
    user_id: int
    type: str
    inputs: Dict[str, Any]


class CalculationUpdate(BaseModel):
    type: Optional[str] = None
    inputs: Optional[Dict[str, Any]] = None


class CalculationRead(BaseModel):
    id: int
    user_id: int
    type: str
    inputs: Dict[str, Any]
    result: Optional[float]
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
