from model.xgboost_classifier import XGBoostModel
from backend.src.utils import preprocess_input, hash_user_key
from backend.src.db import ShelveDB
from backend.src import schemas

class PredictCreditService:
    def __init__(self, model: XGBoostModel):
        self._classifier = model

    def predict(self, data: schemas.PredictionRequest):
        preprocessed_data = preprocess_input(data)
        prediction = self._classifier.predict(preprocessed_data)
        return prediction['prediction'], prediction['probability']


class ExplainResultsService:
    def __init__(self, model: XGBoostModel):
        self._classifier = model

    def explain_prediction(self, data: schemas.PredictionRequest):
        preprocessed_data = preprocess_input(data)
        importance_levels = self._classifier.get_importance_values(preprocessed_data)
        print(importance_levels)
        return importance_levels
    

class UserDataService:
    def __init__(self, db: ShelveDB):
        self._db = db
    
    def store_data(self, data: schemas.PredictionRequest):
        user: schemas.User = data.user
        user_key = hash_user_key(user.name, user.email)

        value_data = data.model_dump()
        value_data.pop("user")
        try:
            self._db.write(user_key, value_data)
        except Exception as e:
            print(str(e))


class CreditApplicationService:
    def __init__(self, db: ShelveDB):
        self._db = db
    
    def create_application(self, data: schemas.CreditApplication):
        user: schemas.User = data.user.model_dump_json()
        try:
            self._db.write(user, data.text)
        except Exception as e:
            print(str(e))


class ReportModelService:
    def __init__(self, db: ShelveDB):
        self._db = db
    
    def report_model(self, data: schemas.ModelReport):
        user: schemas.User = data.user.model_dump_json()
        try:
            self._db.write(user, {"issue_type": data.issue_type, "text": data.text})
        except Exception as e:
            print(str(e))
