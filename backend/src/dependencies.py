from backend.src.services import PredictCreditService, ExplainResultsService
from fastapi import Request

def get_predict_credit_service(request: Request) -> PredictCreditService:
    return PredictCreditService(model=request.app.state.classifier)

def get_explain_results_service(request: Request) -> ExplainResultsService:
    return ExplainResultsService(model=request.app.state.classifier)
