from xgboost import XGBClassifier
import typing as tp
import numpy as np
from backend.src.schemas import PredictionRequest

class XGBoostModel:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(XGBoostModel, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self, model_path: str = "model/xgboost_model.json"):
        if not hasattr(self, "_model"):
            self._model = XGBClassifier()
            self._model.load_model(model_path)
            print(f"Model loaded from {model_path}")

    def predict(self, features: np.ndarray) -> dict:
        prediction = self._model.predict(features)
        probabilities = self._model.predict_proba(features).tolist()

        return {
            "prediction": int(prediction[0]),
            "probability": probabilities[0][0]
        }