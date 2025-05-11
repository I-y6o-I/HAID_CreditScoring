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
    yield

app = FastAPI(docs_url="/", lifespan=startup_envents)

app.include_router(router)
