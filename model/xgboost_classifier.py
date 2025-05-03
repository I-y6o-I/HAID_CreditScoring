from xgboost import XGBClassifier
import typing as tp
import numpy as np
from backend.src.schemas import PredictionRequest
import shap

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

            self.explainer = shap.Explainer(self._model)

    def predict(self, features: np.ndarray) -> dict:
        prediction = self._model.predict(features)
        probabilities = self._model.predict_proba(features).tolist()

        return {
            "prediction": int(prediction[0]),
            "probability": probabilities[0][0],
        }
    
    def get_importance_values(self, features: np.ndarray) -> tp.Dict[str, int]:
        shap_values = self.explainer(features).values.flatten()
        feature_names = self._model.get_booster().feature_names

        levels = []

        neutral_threshold = np.percentile(np.abs(shap_values), 20)
        max_pos = shap_values[shap_values > 0].max(initial=0)
        max_neg = shap_values[shap_values < 0].min(initial=0)

        for val in shap_values:
            if abs(val) < neutral_threshold:
                levels.append(0)
            elif val > 0:
                if val > 0.5 * max_pos:
                    levels.append(-2)
                else:
                    levels.append(-1)
            else:
                if val < 0.5 * max_neg:
                    levels.append(2)
                else:
                    levels.append(1)

        importance_levels = {
            feature_names[i]: levels[i] for i in range(len(feature_names))
        }

        return importance_levels