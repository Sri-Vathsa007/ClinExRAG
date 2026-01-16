from pydantic import BaseModel, Field
from typing import Optional, List

class PatientContext(BaseModel):
    age: int = Field(..., ge=0, le=120)
    sex: str = Field(..., description="female/male/other")
    pregnant: Optional[bool] = None

    symptoms: List[str] = Field(default_factory=list, description="e.g., dysuria, frequency, urgency")
    red_flags: List[str] = Field(default_factory=list, description="e.g., fever, flank_pain, rigors, sepsis_signs")

    penicillin_allergy: Optional[bool] = None
    other_allergies: List[str] = Field(default_factory=list)

    egfr: Optional[float] = Field(default=None, description="renal function if available")

class CDSRequest(BaseModel):
    question: str
    patient: PatientContext
