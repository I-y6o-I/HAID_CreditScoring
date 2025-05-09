import numpy as np
from backend.src.schemas import PredictionRequest

def preprocess_input(data: PredictionRequest) -> np.ndarray:
    response = np.array([
        data.code_gender,
        data.flag_own_car,
        data.flag_own_realty,
        data.cnt_children,
        data.amt_income_total, 
        data.code_income_type,
        data.code_education_type,
        data.code_family_status,
        data.code_housing_type,
        data.days_birth,
        data.days_employed,
        data.code_occupation_type,
        data.cnt_family_members
    ]).reshape(1, -1)

    return response.reshape(1, -1)