import numpy as np
from backend.src.schemas import PredictionRequest
from model.xgboost_classifier import XGBoostModel

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

class PredictCreditService:
    def __init__(self, model):
        self.classifier = model
    
    def predict(self, data: PredictionRequest):
        preprocessed_data = preprocess_input(data)
        prediction = self.classifier.predict(preprocessed_data)
        return prediction['prediction'], prediction['probability']
