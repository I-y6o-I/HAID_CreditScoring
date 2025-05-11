from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from pydantic import BaseModel
from typing import Dict, Optional
import numpy as np

# Модель данных для запроса предсказания
class PredictionRequest(BaseModel):
    code_gender: int
    days_birth: int
    amt_income_total: float
    days_employed: int
    flag_own_car: bool
    flag_own_realty: bool
    code_income_type: int
    code_education_type: int
    code_family_status: int
    cnt_family_members: int
    cnt_children: int
    code_housing_type: int
    code_occupation_type: int

# Модель для ответа с важностью фич
class FeatureImportanceResponse(BaseModel):
    code_gender: float
    days_birth: float
    amt_income_total: float
    days_employed: float
    flag_own_car: float
    flag_own_realty: float
    code_income_type: float
    code_education_type: float
    code_family_status: float
    cnt_family_members: float
    cnt_children: float
    code_housing_type: float
    code_occupation_type: float

# Заглушка модели XGBoost
class XGBoostModel:
    def __init__(self):
        # В реальном приложении здесь была бы загрузка модели
        pass
    
    def predict(self, data: Dict) -> Dict:
        """Возвращает предсказание и вероятность"""
        # Заглушка для демонстрации
        return {
            "prediction": np.random.randint(0, 2),
            "probability": np.random.uniform(0.5, 0.95)
        }
    
    def get_importance_values(self, data: Dict) -> Dict[str, float]:
        """Возвращает важность фич в диапазоне [-2, 2]"""
        # Заглушка с случайными значениями
        features = [
            'code_gender', 'days_birth', 'amt_income_total', 'days_employed',
            'flag_own_car', 'flag_own_realty', 'code_income_type',
            'code_education_type', 'code_family_status', 'cnt_family_members',
            'cnt_children', 'code_housing_type', 'code_occupation_type'
        ]
        return {feature: np.random.uniform(-2, 2) for feature in features}

# Инициализация приложения
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Инициализация модели при старте
    app.state.model = XGBoostModel()
    yield
    # Очистка ресурсов при завершении

app = FastAPI(
    title="Credit Scoring API",
    description="API для предсказания кредитного скоринга с объяснением модели",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Root endpoint
@app.get("/")
async def root():
    return {
        "message": "Добро пожаловать в Credit Scoring API",
        "docs": "/docs",
        "redoc": "/redoc"
    }

# Endpoint для проверки работы сервера
@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "model_loaded": hasattr(app.state, "model")
    }

# Endpoint для получения информации о модели
@app.get("/api/model-info", tags=["Model"])
async def model_info():
    return {
        "model_type": "XGBoost Classifier",
        "version": "1.0",
        "input_features": [
            "code_gender", "days_birth", "amt_income_total",
            "days_employed", "flag_own_car", "flag_own_realty",
            "code_education_type", "cnt_children"
        ],
        "prediction_output": {
            "prediction": "int (0/1)",
            "probability": "float (0-1)",
            "feature_importance": "dict (values from -2 to 2)"
        }
    }

# Endpoint для обработки согласия на хранение данных
@app.post("/api/consent", tags=["Consent"])
async def handle_consent(consent: bool):
    # В реальном приложении здесь бы сохранялись предпочтения пользователя
    return {
        "status": "success",
        "message": "Consent preference saved",
        "consent_given": consent
    }

# Endpoint для предсказания
@app.post("/api/predict", response_model=Dict[str, float], tags=["Prediction"])
async def predict(request: PredictionRequest):
    try:
        # Преобразуем Pydantic модель в dict
        input_data = request.dict()
        
        # Получаем предсказание
        prediction = app.state.model.predict(input_data)
        
        # Получаем важность фич
        importance = app.state.model.get_importance_values(input_data)
        
        return {
            "prediction": prediction["prediction"],
            "probability": prediction["probability"],
            **importance
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Endpoint только для важности фич
@app.post("/api/explain", response_model=FeatureImportanceResponse, tags=["Explanation"])
async def explain(request: PredictionRequest):
    try:
        input_data = request.dict()
        importance = app.state.model.get_importance_values(input_data)
        return importance
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)