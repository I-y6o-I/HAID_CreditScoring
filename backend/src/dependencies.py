from backend.src.services import PredictCreditService
from fastapi import Request

def get_predict_credit_service(request: Request) -> PredictCreditService:
    return PredictCreditService(model=request.app.state.classifier)
