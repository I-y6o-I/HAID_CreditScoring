from fastapi import FastAPI
from contextlib import asynccontextmanager
from model.xgboost_classifier import XGBoostModel
from backend.src.handlers import router


@asynccontextmanager
async def startup_envents(app: FastAPI):
    app.state.classifier = XGBoostModel()
    yield

app = FastAPI(docs_url="/", lifespan=startup_envents)
app.include_router(router)
