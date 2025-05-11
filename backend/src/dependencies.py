from fastapi import Request
from backend.src import services

def get_predict_credit_service(request: Request) -> services.PredictCreditService:
    return services.PredictCreditService(model=request.app.state.classifier)

def get_explain_results_service(request: Request) -> services.ExplainResultsService:
    return services.ExplainResultsService(model=request.app.state.classifier)

def get_user_data_service(request: Request) -> services.UserDataService:
    return services.UserDataService(db=request.app.state.user_data_db)

def get_credit_application_service(request: Request) -> services.CreditApplicationService:
    return services.CreditApplicationService(db=request.app.state.credit_application_db)

def get_report_model_service(request: Request) -> services.ReportModelService:
    return services.ReportModelService(db=request.app.state.model_report_db)
