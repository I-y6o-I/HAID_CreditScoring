from fastapi import APIRouter, Form, Depends, HTTPException, Request, Response
from backend.src.schemas import PredictionRequest, PredictionResponse, FeatureExplainLevels
from backend.src.services import PredictCreditService, ExplainResultsService, UserDataService
from backend.src import dependencies

router = APIRouter(tags=["Model"])

@router.post("/predict", response_model=PredictionResponse)
async def predict_credit_approve(
    request: PredictionRequest,
    predict_service: PredictCreditService = Depends(dependencies.get_predict_credit_service),
) -> PredictionResponse:
    try:
        pred, proba = predict_service.predict(request)
        return PredictionResponse(pred=pred, proba=proba)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

@router.post("/explain", response_model=FeatureExplainLevels)
async def predict_credit_approve(
    request: PredictionRequest,
    explain_service: ExplainResultsService = Depends(dependencies.get_explain_results_service)
) -> FeatureExplainLevels:
    try:
        importance_levels = explain_service.explain_prediction(request)
        return FeatureExplainLevels(**importance_levels)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

@router.post("/store_user_data")
async def store_user_data(
    request: PredictionRequest,
    fastapi_request: Request,
    user_data_service: UserDataService = Depends(dependencies.get_user_data_service)
):
    try:
        store_data = fastapi_request.cookies.get("store_data", "false").lower() == "true"
        if store_data:
            user_data_service.store_data(request)
            return {"message": "Data stored"}
        else:
            return {"message": "Data is not stored due to settings"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/update-settings")
async def update_settings(store_data: bool, response: Response):
    response.set_cookie(key="store_data", value=str(store_data).lower(), httponly=False, secure=False, samesite="Lax")
    return {"message": "Settings updated successfully", "store_data": store_data}