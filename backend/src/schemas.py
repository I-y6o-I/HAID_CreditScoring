from pydantic import BaseModel
import typing as tp


class PredictionRequest(BaseModel):
    code_gender: int
    days_birth: int
    amt_income_total: int
    days_employed: int
    flag_own_car: bool
    flag_own_realty: bool
    code_income_type: int
    code_education_type: int
    code_family_status: int
    cnt_family_members: int
    cnt_children: int
    code_housing_type: int
    code_occupation_type: int


class PredictionResponse(BaseModel):
    pred: int
    proba: float
    