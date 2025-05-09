import streamlit as st
import pandas as pd
import requests
import matplotlib.pyplot as plt
from greetings import greetings_page

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

if "page" not in st.session_state:
    st.session_state["page"] = "greetings"

if st.session_state["page"] == "greetings":
    greetings_page()
elif st.session_state["page"] == "main":
    st.title("💳 Credit Scoring Assessment")

    if st.button("Home"):
        st.session_state["page"] = "greetings"
        st.rerun()

    st.markdown("""
    <p style='font-size: 18px; color: #7f8c8d;'>
        Enter your financial and personal information to evaluate your credit approval chances. 
        The app uses an AI model to predict the outcome and explain which factors influenced it.
    </p>
    """, unsafe_allow_html=True)

    st.divider()

    with st.form("credit_form"):
        st.subheader("🔍 Enter your information")

        col1, col2 = st.columns(2)

        with col1:
            name = st.text_input("Full Name")
            code_gender = st.selectbox("Gender", options=[0, 1], format_func=lambda x: "Male" if x == 1 else "Female")
            flag_own_car = st.selectbox("Owns a Car", options=[0, 1], format_func=lambda x: "Yes" if x == 1 else "No")
            flag_own_realty = st.selectbox("Owns Realty", options=[0, 1], format_func=lambda x: "Yes" if x == 1 else "No")
            cnt_children = st.number_input("Number of Children", min_value=0, value=0)
            amt_income_total = st.number_input("Annual Income ($)", min_value=0, value=50000)

        with col2:
            email = st.text_input("Email")
            code_income_type = st.selectbox("Income Type", options=list(CODE_INCOME_TYPE.keys()))
            code_education_type = st.selectbox("Education Type", options=list(CODE_EDUCATION_TYPE.keys()))
            code_family_status = st.selectbox("Family Status", options=list(CODE_FAMILY_STATUS.keys()))
            code_housing_type = st.selectbox("Housing Type", options=list(CODE_HOUSING_TYPE.keys()))
            cnt_family_members = st.number_input("Number of Family Members", min_value=1, value=1)

        days_birth = st.slider("Age (in Days)", min_value=-36500, max_value=-6570, value=-10950)  # Example: -10950 = 30 years
        days_employed = st.slider("Days Employed", min_value=-20000, max_value=0, value=-3650)  # Example: -3650 = 10 years
        code_occupation_type = st.selectbox("Occupation Type", options=list(CODE_OCCUPATION_TYPE.keys()))

        submitted = st.form_submit_button("Evaluate Credit Score")

    if submitted:
        input_payload = {
            "user": {
                "name": name,
                "email": email
            },
            "code_gender": code_gender,
            "flag_own_car": flag_own_car,
            "flag_own_realty": flag_own_realty,
            "cnt_children": cnt_children,
            "amt_income_total": amt_income_total,
            "code_income_type": CODE_INCOME_TYPE[code_income_type],
            "code_education_type": CODE_EDUCATION_TYPE[code_education_type],
            "code_family_status": CODE_FAMILY_STATUS[code_family_status],
            "code_housing_type": CODE_HOUSING_TYPE[code_housing_type],
            "days_birth": days_birth,
            "days_employed": days_employed,
            "code_occupation_type": CODE_OCCUPATION_TYPE[code_occupation_type],
            "cnt_family_members": cnt_family_members
        }

        with st.spinner("Evaluating..."):
            predict_response = requests_session.post(f"{API_BASE_URL}/predict", json=input_payload)
            result = predict_response.json()

            probability = result["proba"]
            decision = result["pred"]

            st.subheader("📊 Prediction Result")
            st.metric("Credit Approval Probability", f"{probability * 100:.1f}%")
            if decision == 0:
                st.success("✅ Likely Approved")
            else:
                st.error("❌ Likely Declined")

            requests_session.post(
                f"{API_BASE_URL}/update-settings",
                params={
                    "store_data": True
                }
            )

            requests_session.post(
                f"{API_BASE_URL}/store_user_data",
                json=input_payload
            )


            explain_response = requests_session.post(
                f"{API_BASE_URL}/explain",
                json=input_payload
            )
            explanation = explain_response.json()

            st.markdown("#### 🔎 Feature Contributions")
            importances = pd.Series(explanation).sort_values()
            fig, ax = plt.subplots(figsize=(6, 4))
            importances.plot(kind='barh', color=['#27ae60' if v > 0 else '#c0392b' for v in importances.values], ax=ax)
            ax.set_xlabel("Importance")
            st.pyplot(fig)