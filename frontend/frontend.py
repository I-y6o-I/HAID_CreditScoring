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

AGE_GROUPS = {
    0: "18-22",
    1: "23-29",
    2: "30-34",
    3: "35-39",
    4: "40-44",
    5: "45-49",
    6: "50-54",
    7: "55-59",
    8: "60-64",
    9: "65-69",
}

YEARS_EMPLOYED_CAT = {
    0: "0",
    1: "1-3",
    3: "4-10",
    2: "10+",
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
            flag_own_car = st.selectbox("Owns a Car", options=[0, 1], format_func=lambda x: "Yes" if x == 1 else "No")
            flag_own_realty = st.selectbox("Owns Realty", options=[0, 1], format_func=lambda x: "Yes" if x == 1 else "No")
            cnt_children = st.number_input("Number of Children", min_value=0, value=0)
            amt_income_total = st.number_input("Annual Income ($)", min_value=0, value=50000)
            cnt_family_members = st.number_input("Number of Family Members", min_value=1, value=1)

        with col2:
            email = st.text_input("Email")
            code_income_type = st.selectbox("Income Type", options=list(CODE_INCOME_TYPE.keys()))
            code_education_type = st.selectbox("Education Type", options=list(CODE_EDUCATION_TYPE.keys()))
            code_family_status = st.selectbox("Family Status", options=list(CODE_FAMILY_STATUS.keys()))
            code_housing_type = st.selectbox("Housing Type", options=list(CODE_HOUSING_TYPE.keys()))

        age_group = st.selectbox("Age Group", options=list(AGE_GROUPS.keys()), format_func=lambda x: AGE_GROUPS[x])
        years_employed_cat = st.selectbox("Years Employed", options=list(YEARS_EMPLOYED_CAT.keys()), format_func=lambda x: YEARS_EMPLOYED_CAT[x])
        code_occupation_type = st.selectbox("Occupation Type", options=list(CODE_OCCUPATION_TYPE.keys()))

        submitted = st.form_submit_button("Evaluate Credit Score")

    if submitted:
        print(age_group, code_education_type)
        input_payload = {
            "user": {
                "name": name,
                "email": email
            },
            "flag_own_car": flag_own_car,
            "flag_own_realty": flag_own_realty,
            "cnt_children": cnt_children,
            "amt_income_total": amt_income_total,
            "code_income_type": CODE_INCOME_TYPE[code_income_type],
            "code_education_type": CODE_EDUCATION_TYPE[code_education_type],
            "code_family_status": CODE_FAMILY_STATUS[code_family_status],
            "code_housing_type": CODE_HOUSING_TYPE[code_housing_type],
            "age_group": age_group,
            "years_employed_cat": years_employed_cat,
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
                f"{API_BASE_URL}/update_settings",
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