from fastapi import APIRouter, Form, Depends, HTTPException
from backend.src.schemas import PredictionRequest, PredictionResponse
from backend.src.dependencies import get_predict_credit_service
from backend.src.services import PredictCreditService

router = APIRouter(tags=["Model"])

@router.post("/predict", response_model=PredictionResponse)
async def predict_credit_approve(
    request: PredictionRequest,
    predict_service: PredictCreditService = Depends(get_predict_credit_service)
):
    try:
        pred, proba = predict_service.predict(request)
        return PredictionResponse(pred=pred, proba=proba)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))