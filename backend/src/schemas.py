from pydantic import BaseModel
import typing as tp


class User(BaseModel):
    name: str
    email: str


class PredictionRequest(BaseModel):
    user: User
    age_group: int
    amt_income_total: int
    years_employed_cat: int
    flag_own_car: bool
    flag_own_realty: bool
    code_income_type: int
    code_education_type: int
    code_family_status: int
    cnt_family_members: int
    cnt_children: int
    code_housing_type: int
    code_occupation_type: int


class FeatureExplainLevels(BaseModel):
    age_group: int
    amt_income_total: int
    years_employed_cat: int
    flag_own_car: int
    flag_own_realty: int
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


class CreditApplication(BaseModel):
    user: User
    text: str


class ModelReport(BaseModel):
    user: User
    text: str
    