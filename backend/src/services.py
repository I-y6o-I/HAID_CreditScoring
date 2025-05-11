from backend.src.schemas import PredictionRequest, User
from model.xgboost_classifier import XGBoostModel
from backend.src.utils import preprocess_input, hash_user_key
from backend.src.db import ShelveDB

class PredictCreditService:
    def __init__(self, model: XGBoostModel):
        self._classifier = model

    def predict(self, data: PredictionRequest):
        preprocessed_data = preprocess_input(data)
        prediction = self._classifier.predict(preprocessed_data)
        return prediction['prediction'], prediction['probability']


class ExplainResultsService:
    def __init__(self, model: XGBoostModel):
        self._classifier = model

    def explain_prediction(self, data: PredictionRequest):
        preprocessed_data = preprocess_input(data)
        importance_levels = self._classifier.get_importance_values(preprocessed_data)
        print(importance_levels)
        return importance_levels
    

class UserDataService:
    def __init__(self, db: ShelveDB):
        self._db = db
    
    def store_data(self, data: PredictionRequest):
        user: User = data.user
        user_key = hash_user_key(user.name, user.email)

        value_data = data.model_dump()
        value_data.pop("user")
        try:
            self._db.write(user_key, value_data)
        except Exception as e:
            print(str(e))
