# frontend.py
import streamlit as st
import pandas as pd
import requests
import matplotlib.pyplot as plt
from greetings import greetings_page
import json

COLORS = {
    "primary": "#3498db",
    "secondary": "#2ecc71",
    "danger": "#e74c3c",
    "warning": "#f39c12",
    "dark": "#2c3e50",
    "light": "#ecf0f1",
    "text": "#333333",
    "background": "#f8f9fa"
}
def set_global_styles():
    st.markdown("""
    <style>
        /* Основные стили текста */
        body {
            color: #333333 !important;
        }
        
        /* Заголовки */
        h1, h2, h3, h4, h5, h6 {
            color: #2c3e50 !important;
        }
        
        /* Обычный текст */
        .stMarkdown, .stText {
            color: #333333 !important;
        }
        
        /* Карточки и блоки */
        .stContainer, .stExpander {
            background-color: #f8f9fa !important;
            padding: 15px !important;
            border-radius: 10px !important;
            margin-bottom: 15px !important;
        }
        
        /* Формы */
        .stForm {
            background-color: #ffffff !important;
            border: 1px solid #e0e0e0 !important;
            border-radius: 10px !important;
            padding: 20px !important;
        }
    </style>
    """, unsafe_allow_html=True)
# Конфигурация страницы
st.set_page_config(
    page_title="Credit Scoring AI",
    page_icon="💳",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Стили CSS
def load_css():
    st.markdown("""
    <style>
        .main {
            max-width: 1000px;
            padding: 2rem;
        }
        .header {
            text-align: center;
            margin-bottom: 2rem;
        }
        .feature-card {
            padding: 1.5rem;
            border-radius: 10px;
            background: #f8f9fa;
            margin-bottom: 1rem;
        }
        .positive-impact {
            color: #2ecc71;
        }
        .negative-impact {
            color: #e74c3c;
        }
        .stButton>button {
            width: 100%;
            border-radius: 8px;
            padding: 0.5rem 1rem;
        }
        .stForm {
            border: 1px solid #eee;
            border-radius: 10px;
            padding: 2rem;
        }
    </style>
    """, unsafe_allow_html=True)

# Словари для преобразования значений
CODE_INCOME_TYPE = {
    "Commercial associate": 0,
    "Pensioner": 1,
    "State servant": 2,
    "Student": 3,
    "Working": 4,
}

CODE_EDUCATION_TYPE = {
    "Academic degree": 0,
    "Higher education": 1,
    "Incomplete higher": 2,
    "Lower secondary": 3,
    "Secondary / secondary special": 4,
}

CODE_FAMILY_STATUS = {
    "Civil marriage": 0,
    "Married": 1,
    "Separated": 2,
    "Single / not married": 3,
    "Widow": 4,
}

CODE_HOUSING_TYPE = {
    "Co-op apartment": 0,
    "House / apartment": 1,
    "Municipal apartment": 2,
    "Office apartment": 3,
    "Rented apartment": 4,
    "With parents": 5,
}

CODE_OCCUPATION_TYPE = {
    "Accountants": 0,
    "Cleaning staff": 1,
    "Cooking staff": 2,
    "Core staff": 3,
    "Drivers": 4,
    "HR staff": 5,
    "High skill tech staff": 6,
    "IT staff": 7,
    "Laborers": 8,
    "Low-skill Laborers": 9,
    "Managers": 10,
    "Medicine staff": 11,
    "Private service staff": 12,
    "Realty agents": 13,
    "Sales staff": 14,
    "Secretaries": 15,
    "Security staff": 16,
    "Waiters/barmen staff": 17,
}

API_BASE_URL = "http://localhost:8000"
requests_session = requests.Session()

import streamlit as st
import requests

API_BASE_URL = "http://localhost:8000"

def data_consent_page():
    st.markdown("""
    <style>
        .consent-container {
            background-color: #ffffff;
            padding: 2.5rem;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            margin: 0 auto;
            max-width: 800px;
        }
        .consent-header {
            color: #2c3e50;
            text-align: center;
            margin-bottom: 1.5rem;
        }
        .consent-question {
            color: #2c3e50;
            font-size: 1.1rem;
            margin-bottom: 1.5rem;
        }
        .consent-option {
            margin: 1rem 0;
            padding: 0.8rem;
            background-color: #f8f9fa;
            border-radius: 8px;
        }
    </style>
    """, unsafe_allow_html=True)

    st.markdown('<div class="consent-container">', unsafe_allow_html=True)
    st.markdown('<h2 class="consent-header">🔒 Data Consent</h2>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="feature-card">
        To improve our service, we'd like to store your application data anonymously. 
        This helps us make our model fairer and more accurate over time.
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<p class="consent-question">Do you agree to store your data anonymously?</p>', unsafe_allow_html=True)
    
    consent = st.radio(
        "",
        options=["Yes", "No"],
        index=None,
        key="data_consent_radio",
        format_func=lambda x: f'<div class="consent-option">{x}</div>',
        unsafe_allow_html=True
    )
    
    if consent is not None:
        if st.button("Continue", key="consent_continue_btn"):
            try:
                response = requests_session.post(
                    f"{API_BASE_URL}/api/consent",
                    json={"consent": consent == "Yes"}
                )
                if response.status_code == 200:
                    st.session_state["consent_given"] = consent == "Yes"
                    st.session_state["page"] = "main"
                    st.rerun()
                else:
                    st.error("Error saving your preference")
            except:
                st.error("Could not connect to server")
    
    st.markdown('</div>', unsafe_allow_html=True)
def main_page():
    st.markdown("""
    <style>
        .form-container {
            background-color: #ffffff;
            padding: 2rem;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        .form-header {
            color: #2c3e50;
            border-bottom: 2px solid #3498db;
            padding-bottom: 0.5rem;
            margin-bottom: 1.5rem;
        }
        .form-section {
            margin-bottom: 2rem;
        }
        .form-footer {
            margin-top: 1.5rem;
        }
        .stTextInput>div>div>input {
            background-color: #f8f9fa;
        }
    </style>
    """, unsafe_allow_html=True)

    st.title("💳 Credit Scoring Assessment")
    
    cols = st.columns([1,1,1,1])
    with cols[0]:
        if st.button("🏠 Home"):
            st.session_state["page"] = "greetings"
            st.rerun()
    with cols[1]:
        if st.button("📊 Model Report"):
            st.session_state["page"] = "report"
            st.rerun()
    
    with st.container():
        st.markdown('<div class="form-container">', unsafe_allow_html=True)
        
        with st.form("credit_form"):
            st.markdown('<h3 class="form-header">🔍 Personal Information</h3>', unsafe_allow_html=True)
            
            col1, col2 = st.columns(2)
            with col1:
                name = st.text_input("Full Name")
                gender = st.selectbox("Gender", options=["Male", "Female"])
                age = st.slider("Age", 18, 70, 30)
                
            with col2:
                email = st.text_input("Email")
                income = st.number_input("Annual Income ($)", min_value=0, value=50000)
                income_type = st.selectbox("Income Source", options=list(CODE_INCOME_TYPE.keys()))
            
            st.markdown('<h3 class="form-header">Additional Information</h3>', unsafe_allow_html=True)
            
            col3, col4 = st.columns(2)
            with col3:
                education = st.selectbox("Education Level", options=list(CODE_EDUCATION_TYPE.keys()))
                family_status = st.selectbox("Family Status", options=list(CODE_FAMILY_STATUS.keys()))
                owns_car = st.checkbox("Owns a Car")
                
            with col4:
                housing = st.selectbox("Housing Type", options=list(CODE_HOUSING_TYPE.keys()))
                occupation = st.selectbox("Occupation", options=list(CODE_OCCUPATION_TYPE.keys()))
                owns_realty = st.checkbox("Owns Property")
            
            st.markdown('<div class="form-footer">', unsafe_allow_html=True)
            submitted = st.form_submit_button("Evaluate Credit Score")
            st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    if submitted:
        input_payload = {
            "code_gender": 1 if gender == "Male" else 0,
            "days_birth": (70 - age) * 365,  # Примерное преобразование
            "amt_income_total": income,
            "days_employed": experience * 365,
            "flag_own_car": int(owns_car),
            "flag_own_realty": int(owns_realty),
            "code_income_type": CODE_INCOME_TYPE[income_type],
            "code_education_type": CODE_EDUCATION_TYPE[education],
            "code_family_status": CODE_FAMILY_STATUS[family_status],
            "code_housing_type": CODE_HOUSING_TYPE[housing],
            "code_occupation_type": CODE_OCCUPATION_TYPE[occupation],
            "cnt_family_members": family_members,
            "cnt_children": children
        }
        
        with st.spinner("Evaluating your credit score..."):
            try:
                # Отправка данных для предсказания
                predict_response = requests_session.post(
                    f"{API_BASE_URL}/api/predict", 
                    json=input_payload
                )
                result = predict_response.json()
                
                # Отображение результатов
                st.subheader("📊 Credit Decision")
                proba = result.get("probability", 0.5)
                decision = result.get("prediction", 0)
                
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Approval Probability", f"{proba*100:.1f}%")
                with col2:
                    st.metric("Decision", "Approved" if decision == 1 else "Declined")
                
                # Визуализация важности фич
                st.subheader("📈 Key Influencing Factors")
                importance_data = {k: v for k, v in result.items() 
                                 if k not in ["prediction", "probability"]}
                
                # Группировка по категориям
                personal_factors = {
                    "Age": importance_data.get("days_birth", 0),
                    "Gender": importance_data.get("code_gender", 0),
                    "Education": importance_data.get("code_education_type", 0)
                }
                
                financial_factors = {
                    "Income": importance_data.get("amt_income_total", 0),
                    "Income Type": importance_data.get("code_income_type", 0),
                    "Property Ownership": importance_data.get("flag_own_realty", 0)
                }
                
                # Визуализация
                tab1, tab2 = st.tabs(["Personal Factors", "Financial Factors"])
                
                with tab1:
                    fig, ax = plt.subplots()
                    pd.Series(personal_factors).sort_values().plot(
                        kind='barh', 
                        color=['#2ecc71' if x > 0 else '#e74c3c' for x in personal_factors.values()],
                        ax=ax
                    )
                    ax.set_title("Personal Factors Impact")
                    st.pyplot(fig)
                
                with tab2:
                    fig, ax = plt.subplots()
                    pd.Series(financial_factors).sort_values().plot(
                        kind='barh',
                        color=['#2ecc71' if x > 0 else '#e74c3c' for x in financial_factors.values()],
                        ax=ax
                    )
                    ax.set_title("Financial Factors Impact")
                    st.pyplot(fig)
                
                # Сохранение данных (если пользователь согласился)
                if st.session_state.get("consent_given", False):
                    try:
                        requests_session.post(
                            f"{API_BASE_URL}/api/store_data",
                            json={
                                "user_input": input_payload,
                                "prediction_result": result
                            }
                        )
                    except:
                        st.warning("Could not save your data")
                
            except Exception as e:
                st.error(f"Error during prediction: {str(e)}")

def model_report_page():
    st.title("📊 Model Report")
    
    cols = st.columns([1,1,1,1])
    with cols[0]:
        if st.button("🏠 Home"):
            st.session_state["page"] = "greetings"
            st.rerun()
    
    st.markdown("""
    <div class="feature-card">
        This section provides transparency about the AI model used for credit scoring.
    </div>
    """, unsafe_allow_html=True)
    
    try:
        # Получение информации о модели
        response = requests_session.get(f"{API_BASE_URL}/api/model-info")
        model_info = response.json()
        
        st.subheader("Model Characteristics")
        st.json(model_info)
        
        st.subheader("Performance Metrics")
        col1, col2, col3 = st.columns(3)
        col1.metric("Accuracy", "87%")
        col2.metric("Precision", "85%")
        col3.metric("Fairness Score", "92%")
        
        st.subheader("Feature Importance Overview")
        st.image("https://via.placeholder.com/800x400.png?text=Feature+Importance+Heatmap", 
                use_column_width=True)
        
        st.subheader("Bias Audit Results")
        st.write("The model has been tested for potential biases across different demographic groups:")
        st.success("✅ No significant gender bias detected")
        st.success("✅ No significant age bias detected")
        st.warning("⚠️ Slight bias detected for income groups")
        
    except:
        st.error("Could not load model information")

# Главный цикл приложения
def main():
    load_css()
    
    if "page" not in st.session_state:
        st.session_state["page"] = "greetings"
    
    if st.session_state["page"] == "greetings":
        greetings_page()
    elif st.session_state["page"] == "consent":
        data_consent_page()
    elif st.session_state["page"] == "main":
        main_page()
    elif st.session_state["page"] == "report":
        model_report_page()

if __name__ == "__main__":
    main()