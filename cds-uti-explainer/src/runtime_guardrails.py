from typing import Tuple, List
from src.runtime_schema import PatientContext

def check_missing_critical(patient: PatientContext) -> List[str]:
    missing = []
    # For many antibiotic decisions you want pregnancy + allergy + renal function.
    if patient.pregnant is None:
        missing.append("pregnancy status")
    if patient.penicillin_allergy is None:
        missing.append("penicillin allergy status")
    if patient.egfr is None:
        missing.append("eGFR / renal function")
    return missing

def check_escalation(patient: PatientContext) -> Tuple[bool, str]:
    # Red flags suggest upper UTI / sepsis risk → escalate rather than recommend.
    rf = set([x.lower() for x in patient.red_flags])
    if any(x in rf for x in ["fever", "flank_pain", "rigors", "sepsis_signs"]):
        return True, "Red flags present (possible pyelonephritis or serious illness). Escalate to urgent clinical evaluation."
    return False, ""
