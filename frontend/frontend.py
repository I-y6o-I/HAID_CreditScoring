# frontend.py
import streamlit as st
import pandas as pd
import requests
from pydantic import BaseModel, ValidationError
from typing import Optional

# Удаляем все импорты связанные с backend
# Добавляем модели данных которые раньше были в backend

class UserData(BaseModel):
    name: str
    email: str

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
    code_housing_type: int
    code_occupation_type: int
    cnt_family_members: int
    cnt_children: int
    user: UserData

# Конфигурация и стили остаются без изменений
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

st.set_page_config(
    page_title="Credit Scoring AI",
    page_icon="💳",
    layout="wide",
    initial_sidebar_state="expanded"
)

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

def greetings_page():
    st.title("Welcome to Credit Scoring AI")
    st.write("This application helps you evaluate your creditworthiness.")
    
    if st.button("Get Started"):
        st.session_state["page"] = "consent"
        st.rerun()

def data_consent_page():
    st.markdown("""
    <style>
        .consent-container {
            background-color: #ffffff;
            padding: 2rem;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            margin: 0 auto;
            max-width: 800px;
        }
        .consent-header {
            color: #2c3e50 !important;
            text-align: center;
            margin-bottom: 1.5rem;
        }
        .consent-description {
            color: #2c3e50 !important;
            margin-bottom: 1.5rem;
        }
        .stRadio > div {
            padding: 10px;
            border-radius: 8px;
        }
        .stButton>button {
            background-color: #3498db !important;
            color: white !important;
        }
    </style>
    """, unsafe_allow_html=True)

    st.markdown('<div class="consent-container">', unsafe_allow_html=True)
    st.markdown('<h2 class="consent-header">🔒 Data Consent</h2>', unsafe_allow_html=True)
    
    st.markdown("""
    <p class="consent-description">
        To improve our service, we'd like to store your application data anonymously. 
        This helps us make our model fairer and more accurate over time.
    </p>
    """, unsafe_allow_html=True)

    consent = st.radio(
        "Do you agree to store your data anonymously?",
        options=["Yes", "No"],
        index=None,
        key="data_consent_radio"
    )
    
    if consent is not None and st.button("Continue", key="consent_continue_btn"):
        try:
            # Преобразуем выбор в строку 'true'/'false' как требуется API
            store_data = 'true' if consent == 'Yes' else 'false'
            
            # Отправляем запрос с query-параметром
            response = requests_session.post(
                f"{API_BASE_URL}/update-settings?store_data={store_data}",
                timeout=5
            )
            
            # Проверяем ответ
            if response.status_code == 200:
                st.session_state["consent_given"] = consent == "Yes"
                st.session_state["page"] = "main"
                st.rerun()
            else:
                st.error(
                    f"Error saving preference. "
                    f"Status code: {response.status_code}, "
                    f"Response: {response.text}"
                )
                
        except requests.exceptions.RequestException as e:
            st.error(f"Connection error: {str(e)}")
        except Exception as e:
            st.error(f"An unexpected error occurred: {str(e)}")
    
    st.markdown('</div>', unsafe_allow_html=True)
def main_page():
    st.markdown("""
    <style>
        /* Основные стили */
        html, body, .stApp {
            background-color: #f5f5f5 !important;
            color: #333333 !important;
        }
        
        /* Карточки */
        .form-container, .result-card {
            background-color: #ffffff !important;
            border-radius: 10px;
            padding: 2rem;
            margin-bottom: 1.5rem;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            border: 1px solid #e0e0e0;
        }
        
        /* Текст */
        h1, h2, h3, h4, h5, h6, p, div, span, label {
            color: #333333 !important;
        }
        
        /* Элементы формы */
        .stTextInput input, .stNumberInput input, 
        .stSelectbox select, .stSlider div {
            color: #333333 !important;
            background-color: #ffffff !important;
        }
        
        /* Кнопки */
        .stButton>button {
            background-color: #3498db !important;
            color: white !important;
            border: none;
            font-weight: bold;
        }
        
        /* Чекбоксы */
        .stCheckbox>label {
            color: #333333 !important;
        }
        
        /* Статусы */
        .positive {
            color: #27ae60 !important;
            font-weight: bold;
        }
        .negative {
            color: #e74c3c !important;
            font-weight: bold;
        }
    </style>
    """, unsafe_allow_html=True)

    st.title("💳 Credit Scoring Assessment")
    
    if st.button("🏠 Home"):
        st.session_state["page"] = "greetings"
        st.rerun()
    
    # Форма ввода данных
    with st.container():
        st.markdown('<div class="form-container">', unsafe_allow_html=True)
        
        with st.form("credit_form"):
            st.markdown('<h3>Personal Information</h3>', unsafe_allow_html=True)
            
            col1, col2 = st.columns(2)
            with col1:
                name = st.text_input("Full Name", key="name_input")
                gender_option = st.selectbox("Gender", options=["Male", "Female"], key="gender_select")
                code_gender = 1 if gender_option == "Male" else 0
                days_birth = st.slider("Age (in days)", 0, 30000, 10000, key="age_slider")
                cnt_children = st.number_input("Number of Children", min_value=0, value=0, key="children_input")
                
            with col2:
                email = st.text_input("Email", key="email_input")
                amt_income_total = st.number_input("Annual Income ($)", min_value=0, value=50000, key="income_input")
                income_type = st.selectbox("Income Type", options=list(CODE_INCOME_TYPE.keys()), key="income_type_select")
                code_income_type = CODE_INCOME_TYPE[income_type]
            
            st.markdown('<h3>Additional Information</h3>', unsafe_allow_html=True)
            
            col3, col4 = st.columns(2)
            with col3:
                education_type = st.selectbox("Education", options=list(CODE_EDUCATION_TYPE.keys()), key="education_select")
                code_education_type = CODE_EDUCATION_TYPE[education_type]
                family_status = st.selectbox("Family Status", options=list(CODE_FAMILY_STATUS.keys()), key="family_select")
                code_family_status = CODE_FAMILY_STATUS[family_status]
                cnt_family_members = st.number_input("Family Members", min_value=1, value=1, key="family_members_input")
                
            with col4:
                housing_type = st.selectbox("Housing Type", options=list(CODE_HOUSING_TYPE.keys()), key="housing_select")
                code_housing_type = CODE_HOUSING_TYPE[housing_type]
                occupation_type = st.selectbox("Occupation", options=list(CODE_OCCUPATION_TYPE.keys()), key="occupation_select")
                code_occupation_type = CODE_OCCUPATION_TYPE[occupation_type]
                days_employed = st.slider("Employment Duration (days)", 0, 20000, 1000, key="employed_slider")
            
            # Чекбоксы с подписями
            flag_own_car = st.checkbox("I own a car", key="car_checkbox")
            flag_own_realty = st.checkbox("I own real estate property", key="realty_checkbox")
            
            submitted = st.form_submit_button("Evaluate Credit Score", type="primary")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Обработка результатов
    if submitted:
        try:
            request_data = {
                "code_gender": code_gender,
                "days_birth": days_birth,
                "amt_income_total": float(amt_income_total),
                "days_employed": days_employed,
                "flag_own_car": flag_own_car,
                "flag_own_realty": flag_own_realty,
                "code_income_type": code_income_type,
                "code_education_type": code_education_type,
                "code_family_status": code_family_status,
                "code_housing_type": code_housing_type,
                "code_occupation_type": code_occupation_type,
                "cnt_family_members": cnt_family_members,
                "cnt_children": cnt_children,
                "user": {
                    "name": name,
                    "email": email
                }
            }
            
            with st.spinner("Processing your application..."):
                response = requests_session.post(
                    f"{API_BASE_URL}/predict",
                    json=request_data,
                    timeout=10
                )
                
                if response.status_code == 200:
                    result = response.json()
                    st.session_state["last_result"] = result
                    
                    prediction = result.get("pred", 0)
                    probability = result.get("proba", 0.0)
                    
                    with st.container():
                        st.markdown('<div class="result-card">', unsafe_allow_html=True)
                        
                        if prediction == 1:
                            st.markdown(f'<h3 class="positive">Approved ({(probability*100):.1f}%)</h3>', 
                                      unsafe_allow_html=True)
                        else:
                            st.markdown(f'<h3 class="negative">Denied ({(100 - probability*100):.1f}%)</h3>', 
                                      unsafe_allow_html=True)
                        
                        if st.button("Provide feedback about this decision"):
                            st.session_state["page"] = "feedback"
                            st.rerun()
                        
                        st.markdown('</div>', unsafe_allow_html=True)
                else:
                    st.error(f"API Error: {response.status_code} - {response.text}")
                
        except requests.exceptions.RequestException as e:
            st.error(f"Connection error: {str(e)}")
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
    
    # Показываем последний результат при обновлении страницы
    if "last_result" in st.session_state:
        result = st.session_state["last_result"]
        with st.container():
            st.markdown('<div class="result-card">', unsafe_allow_html=True)
            
            prediction = result.get("pred", 0)
            probability = result.get("proba", 0.0)
            
            if prediction == 1:
                st.markdown(f'<h3 class="positive">Approved ({(probability*100):.1f}%)</h3>', 
                          unsafe_allow_html=True)
            else:
                st.markdown(f'<h3 class="negative">Denied ({(100 - probability*100):.1f}%)</h3>', 
                          unsafe_allow_html=True)
            
            if st.button("Provide feedback about this result"):
                st.session_state["page"] = "feedback"
                st.rerun()
            
            st.markdown('</div>', unsafe_allow_html=True)
                
def feedback_page():
    st.title("📝 Model Feedback")
    
    st.markdown("""
    <style>
        .feedback-form {
            background-color: #ffffff;
            padding: 2rem;
            border-radius: 10px;
            margin: 20px auto;
            max-width: 800px;
        }
    </style>
    """, unsafe_allow_html=True)
    
    with st.container():
        st.markdown('<div class="feedback-form">', unsafe_allow_html=True)
        
        st.write("Help us improve our credit scoring model by providing your feedback!")
        
        with st.form("feedback_form"):
            feedback_type = st.selectbox(
                "Type of feedback",
                options=["Incorrect decision", "Model accuracy", "Feature importance", "Other"]
            )
            
            feedback_text = st.text_area("Your detailed feedback", height=150)
            
            email = st.text_input("Email (optional, if you want us to follow up)")
            
            submitted = st.form_submit_button("Submit Feedback")
            
            if submitted:
                # Здесь можно добавить логику отправки фидбека
                st.success("Thank you for your feedback! We'll use it to improve our model.")
                time.sleep(2)
                st.session_state["page"] = "main"
                st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    if st.button("Back to Main Page"):
        st.session_state["page"] = "main"
        st.rerun()
    
def main():
    load_css()
    set_global_styles()
    
    if "page" not in st.session_state:
        st.session_state["page"] = "greetings"
    
    if st.session_state["page"] == "greetings":
        greetings_page()
    elif st.session_state["page"] == "consent":
        data_consent_page()
    elif st.session_state["page"] == "main":
        main_page()
    elif st.session_state["page"] == "feedback":
        feedback_page()

if __name__ == "__main__":
    main()