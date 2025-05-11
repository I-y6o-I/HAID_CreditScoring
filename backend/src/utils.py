import numpy as np
from backend.src.schemas import PredictionRequest
import hashlib

def preprocess_input(data: PredictionRequest) -> np.ndarray:
    response = np.array([
        data.flag_own_car,
        data.flag_own_realty,
        data.cnt_children,
        data.amt_income_total, 
        data.code_income_type,
        data.code_education_type,
        data.code_family_status,
        data.code_housing_type,
        data.age_group,
        data.years_employed_cat,
        data.code_occupation_type,
        data.cnt_family_members
    ]).reshape(1, -1)

    return response.reshape(1, -1)


def hash_user_key(name: str, email: str) -> str:
    combined = f"{name.lower()}|{email.lower()}"
    hashed_key = hashlib.sha256(combined.encode('utf-8')).hexdigest()
    return hashed_key
