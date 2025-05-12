from fastapi import FastAPI
from contextlib import asynccontextmanager
from model.xgboost_classifier import XGBoostModel
from backend.src.handlers import router
from backend.src.db import ShelveDB
from fastapi.middleware.cors import CORSMiddleware



@asynccontextmanager
async def startup_envents(app: FastAPI):
    app.state.classifier = XGBoostModel()
    app.state.credit_application_db = ShelveDB("credit_application")
    app.state.user_data_db = ShelveDB("user_data")
    app.state.model_report_db = ShelveDB("model_report")
    yield

app = FastAPI(docs_url="/", lifespan=startup_envents)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8501", "http://localhost:8000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(router)
