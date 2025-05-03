from fastapi import APIRouter, Form, Depends, HTTPException
from backend.src.schemas import PredictionRequest, PredictionResponse, FeatureExplainLevels
from backend.src.dependencies import get_predict_credit_service, get_explain_results_service
from backend.src.services import PredictCreditService, ExplainResultsService

router = APIRouter(tags=["Model"])

@router.post("/predict", response_model=PredictionResponse)
async def predict_credit_approve(
    request: PredictionRequest,
    predict_service: PredictCreditService = Depends(get_predict_credit_service)
) -> PredictionResponse:
    try:
        pred, proba = predict_service.predict(request)
        return PredictionResponse(pred=pred, proba=proba)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

@router.post("/explain", response_model=FeatureExplainLevels)
async def predict_credit_approve(
    request: PredictionRequest,
    explain_service: ExplainResultsService = Depends(get_explain_results_service)
) -> FeatureExplainLevels:
    try:
        importance_levels = explain_service.explain_prediction(request)
        return FeatureExplainLevels(**importance_levels)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    