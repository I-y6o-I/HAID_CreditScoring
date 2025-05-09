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

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8501"],  # Streamlit frontend origin
    allow_credentials=True,  # Allow cookies to be sent
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)

app.include_router(router)
