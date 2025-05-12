from fastapi import APIRouter, Form, Depends, HTTPException, Request, Response
from backend.src import services
from backend.src import dependencies
from backend.src import schemas

router = APIRouter(tags=["Model"])

@router.post("/predict", response_model=schemas.PredictionResponse)
async def predict_credit_approve(
    request: schemas.PredictionRequest,
    predict_service: services.PredictCreditService = Depends(dependencies.get_predict_credit_service),
) -> schemas.PredictionResponse:
    try:
        pred, proba = predict_service.predict(request)
        return schemas.PredictionResponse(pred=pred, proba=proba)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

@router.post("/explain", response_model=schemas.FeatureExplainLevels)
async def predict_credit_approve(
    request: schemas.PredictionRequest,
    explain_service: services.ExplainResultsService = Depends(dependencies.get_explain_results_service)
) -> schemas.FeatureExplainLevels:
    try:
        importance_levels = explain_service.explain_prediction(request)
        return schemas.FeatureExplainLevels(**importance_levels)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

@router.post("/store_user_data")
async def store_user_data(
    request: schemas.PredictionRequest,
    fastapi_request: Request,
    user_data_service: services.UserDataService = Depends(dependencies.get_user_data_service)
):
    try:
        store_data = fastapi_request.cookies.get("store_data", "false").lower() == "true"
        print("store", fastapi_request.cookies.get("store_data"))
        if store_data:
            user_data_service.store_data(request)
            return {"message": "Data stored"}
        else:
            return {"message": "Data is not stored due to settings"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

@router.post("/create_application")
async def create_application(
    request: schemas.CreditApplication,
    credit_application_service: services.CreditApplicationService = Depends(dependencies.get_credit_application_service)
):
    try:
        credit_application_service.create_application(request)
        return {"message": "Application created"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

@router.post("/report_model")
async def report_model(
    request: schemas.ModelReport,
    report_model_service: services.ReportModelService = Depends(dependencies.get_report_model_service)
):
    try:
        report_model_service.report_model(request)
        return {"message": "Report created"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/update_settings")
async def update_settings(store_data: bool, response: Response):
    response.set_cookie(key="store_data", value=str(store_data).lower(), httponly=True, secure=False, samesite="None")
    return {"message": "Settings updated successfully", "store_data": store_data}