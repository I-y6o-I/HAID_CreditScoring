import streamlit as st
import pandas as pd
import requests
import matplotlib.pyplot as plt
import seaborn as sns
from greetings import greetings_page

INCOME_TYPES = {
    "Commercial associate": 0,
    "Pensioner": 1,
    "State servant": 2,
    "Student": 3,
    "Working": 4,
}

EDUCATION_TYPES = {
    "Academic degree": 0,
    "Higher education": 1,
    "Incomplete higher": 2,
    "Lower secondary": 3,
    "Secondary / secondary special": 4,
}

FAMILY_STATUSES = {
    "Civil marriage": 0,
    "Married": 1,
    "Separated": 2,
    "Single / not married": 3,
    "Widow": 4,
}

HOUSING_TYPES = {
    "Co-op apartment": 0,
    "House / apartment": 1,
    "Municipal apartment": 2,
    "Office apartment": 3,
    "Rented apartment": 4,
    "With parents": 5,
}

OCCUPATION_TYPES = {
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

EMPLOYMENT_DURATION = {
    0: "No experience",
    1: "1-3 years",
    3: "4-10 years",
    2: "10+ years",
}

API_BASE_URL = "http://localhost:8000"
requests_session = requests.Session()
requests_session.headers.update({"Connection": "keep-alive"})

st.set_page_config(
    page_title="Credit Scoring System",
    page_icon="🏠",
    layout="wide"
)

def plot_feature_importance(importances):
    BG_COLOR = "#0e1117"       # Streamlit dark background
    WIDGET_BG = "#262730"      # Streamlit widget background
    TEXT_COLOR = "#fafafa"     # Light text for contrast
    PRIMARY = "#ff4b4b"        # Streamlit red
    SECONDARY = "#21c354"      # Streamlit green
    GRID_COLOR = "#555555"     # Dark grid lines
    BAR_EDGE = "#444444"       # Bar edge color

    fig = plt.figure(figsize=(10, 6), facecolor=BG_COLOR, dpi=100)
    ax = fig.add_subplot(facecolor=BG_COLOR)
    fig.patch.set_facecolor(BG_COLOR)

    
    feature_names = {
        'amt_income_total': 'Annual Income',
        'code_income_type': 'Income Type',
        'code_education_type': 'Education',
        'age_group': 'Age Group',
        'years_employed_cat': 'Employment',
        'cnt_family_members': 'Family Size',
        'cnt_children': 'Children',
        'flag_own_realty': 'Owns Property',
        'flag_own_car': 'Owns Car',
        'code_family_status': 'Marital Status',
        'code_housing_type': 'Housing',
        'code_occupation_type': 'Occupation'
    }

    df = pd.DataFrame({
        'Factor': [feature_names.get(col, col) for col in importances.index],
        'Impact': importances.values,
        'Effect': ['Positive' if x > 0 else 'Negative' for x in importances.values]
    }).sort_values('Impact', key=abs, ascending=False)

    sns.barplot(
        data=df,
        x='Impact',
        y='Factor',
        hue='Effect',
        palette={'Positive': SECONDARY, 'Negative': PRIMARY},
        ax=ax,
        dodge=False,
        linewidth=0.8,
        edgecolor=BAR_EDGE,
        saturation=0.9
    )

    ax.set_title('Credit Decision Factors', 
                pad=20, fontsize=14, color=TEXT_COLOR, fontweight='bold')
    ax.set_xlabel('Impact Score', fontsize=12, color=TEXT_COLOR)
    ax.set_ylabel('')
    
    ax.tick_params(axis='both', colors=TEXT_COLOR, labelsize=10)
    for spine in ax.spines.values():
        spine.set_color(GRID_COLOR)
    
    ax.axvline(0, color=TEXT_COLOR, linestyle='--', linewidth=1.0, alpha=0.8)
    ax.grid(axis='x', color=GRID_COLOR, linestyle=':', linewidth=0.7, alpha=0.8)

    legend = ax.legend(
        title='Impact Direction',
        facecolor=WIDGET_BG,
        edgecolor=GRID_COLOR,
        title_fontsize=10,
        fontsize=9,
        bbox_to_anchor=(1.02, 1),
        loc='upper left'
    )
    legend.get_title().set_color(TEXT_COLOR)
    for text in legend.get_texts():
        text.set_color(TEXT_COLOR)

    plt.tight_layout()
    return fig


def show_feedback_form(user_data=None):
    """Feedback submission form"""
    st.markdown("---")
    st.subheader("📝 Decision Feedback")
    
    with st.form(key='feedback_form'):
        name = st.text_input("Your Name", value=user_data.get("user", {}).get("name", "") if user_data else "")
        email = st.text_input("Your Email", value=user_data.get("user", {}).get("email", "") if user_data else "")
        
        feedback_type = st.selectbox(
            "Feedback Type",
            options=[
                "Incorrect decision",
                "Issue with factors",
                "Model accuracy",
                "Data privacy",
                "Other"
            ]
        )
        
        feedback_details = st.text_area(
            "Details",
            placeholder="Describe your experience or concern...",
            height=150
        )
        
        submitted = st.form_submit_button("Submit Feedback")
        
        if submitted:
            if not feedback_details:
                st.error("Please provide details")
            else:
                try:
                    feedback_data = {
                        "user": {
                            "name": name,
                            "email": email,
                        },
                        "issue_type": feedback_type,
                        "text": feedback_details,
                    }
                    
                    response = requests_session.post(
                        f"{API_BASE_URL}/report_model",
                        json=feedback_data
                    )
                    
                    if response.status_code == 200:
                        st.session_state["show_feedback"] = 2
                        st.rerun()
                    else:
                        st.error("Submission failed. Please try later.")
                except Exception as e:
                    st.error(f"Connection error: {str(e)}")


def show_credit_form(user_data=None):
    st.markdown("---")
    st.subheader("📝 Contact manager and apply for a credit")
    
    with st.form(key='application_form'):
        name = st.text_input("Your Name", value=user_data.get("user", {}).get("name", "") if user_data else "")
        email = st.text_input("Your Email", value=user_data.get("user", {}).get("email", "") if user_data else "")
        
        
        details = st.text_area(
            "Details",
            placeholder="Provide any useful information...",
            height=150
        )
        
        submitted = st.form_submit_button("Submit Application")

        if st.session_state.get("show_application", 1):
            st.success("Thank you! Manager will contact you soon!")
            return
        
        if submitted:
            if not details:
                st.error("Please provide details")
            else:
                try:
                    feedback_data = {
                        "user": {
                            "name": name,
                            "email": email,
                        },
                        "text": details,
                    }
                    
                    response = requests_session.post(
                        f"{API_BASE_URL}/create_application",
                        json=feedback_data
                    )
                    
                    if response.status_code == 200:
                        st.session_state["show_application"] = 1
                        st.rerun()
                    else:
                        st.error("Submission failed. Please try later.")
                except Exception as e:
                    st.error(f"Connection error: {str(e)}")


def settings_page():
    st.title("⚙️ Settings")
    st.subheader("Manage Your Preferences")
    
    store_data = st.radio(
        "Do you want to help improve our service and share your data?",
        options=["No", "Yes"],
        index=1 if st.session_state.get("store_data") == "Yes" else 0
    )
    
    if st.button("Save"):
        st.session_state["store_data"] = store_data
        st.success("Settings saved!")
        st.session_state["page"] = "main"
        st.rerun()

if "page" not in st.session_state:
    st.session_state["page"] = "greetings"
    st.session_state["show_feedback"] = False
    st.session_state["application_data"] = None
    st.session_state["show_application"] = 0


if st.session_state["page"] == "greetings":
    greetings_page()
elif st.session_state["page"] == "settings":
    settings_page()
elif st.session_state["page"] == "main":
    col1, col2, col3 = st.columns([1, 6.5, 1])
    with col1:
        if st.button("🏠 Home"):
            st.session_state["page"] = "greetings"
            st.rerun()
    with col3:
        with st.popover(label="⚙️ Settings"):
            st.subheader("Settings")
            store_data = st.radio(
                "Do you want to help improve our service and share your data?",
                options=["No", "Yes"],
                index=1 if st.session_state.get("store_data") == "Yes" else 0
            )
            if st.button("Save"):
                st.session_state["store_data"] = store_data
                st.success("Settings saved!")



    st.title("💳 Credit Scoring Assessment")

    st.markdown("""
    <p style='font-size: 18px; color: #7f8c8d;'>
        Enter your information to evaluate credit approval chances. 
        Our AI model predicts outcomes and explains decision factors.
    </p>
    """, unsafe_allow_html=True)

    st.divider()

    with st.form("credit_form"):
        st.subheader("🔍 Your Information")

        col1, col2 = st.columns(2)

        with col1:
            name = st.text_input("Full Name")
            age_group = st.selectbox("Age Group", options=list(AGE_GROUPS.keys()), format_func=lambda x: AGE_GROUPS[x])
            flag_own_car = st.selectbox("Owns a Car", options=[0, 1], format_func=lambda x: "Yes" if x == 1 else "No", index=1)
            flag_own_realty = st.selectbox("Owns Property", options=[0, 1], format_func=lambda x: "Yes" if x == 1 else "No", index=1)
            cnt_children = st.number_input("Number of Children", min_value=0, value=0)
            amt_income_total = st.number_input("Annual Income ($)", min_value=0, value=50000, step=10000)

        with col2:
            email = st.text_input("Email")
            code_income_type = st.selectbox("Income Type", options=list(INCOME_TYPES.keys()))
            code_education_type = st.selectbox("Education Level", options=list(EDUCATION_TYPES.keys()))
            code_family_status = st.selectbox("Marital Status", options=list(FAMILY_STATUSES.keys()))
            code_housing_type = st.selectbox("Housing Type", options=list(HOUSING_TYPES.keys()))
            cnt_family_members = st.number_input("Family Members", min_value=1, value=1)

        years_employed_cat = st.selectbox("Employment Duration", options=list(EMPLOYMENT_DURATION.keys()), format_func=lambda x: EMPLOYMENT_DURATION[x])
        code_occupation_type = st.selectbox("Occupation", options=list(OCCUPATION_TYPES.keys()))

        submitted = st.form_submit_button("Get Credit Score")

    if submitted:
        input_payload = {
            "user": {
                "name": name,
                "email": email
            },
            "flag_own_car": flag_own_car,
            "flag_own_realty": flag_own_realty,
            "cnt_children": cnt_children,
            "amt_income_total": amt_income_total,
            "code_income_type": list(INCOME_TYPES.keys()).index(code_income_type),
            "code_education_type": list(EDUCATION_TYPES.keys()).index(code_education_type),
            "code_family_status": list(FAMILY_STATUSES.keys()).index(code_family_status),
            "code_housing_type": list(HOUSING_TYPES.keys()).index(code_housing_type),
            "age_group": age_group,
            "years_employed_cat": years_employed_cat,
            "code_occupation_type": list(OCCUPATION_TYPES.keys()).index(code_occupation_type),
            "cnt_family_members": cnt_family_members
        }

        st.session_state["application_data"] = input_payload

        with st.spinner("Evaluating..."):
            predict_response = requests_session.post(f"{API_BASE_URL}/predict", json=input_payload)
            result = predict_response.json()

            probability = result["proba"]
            decision = result["pred"]

            st.subheader("📊 Evaluation Result")
            st.metric("Approval Probability", f"{probability * 100:.1f}%")
            if decision == 0:
                st.success("✅ Likely Approved")
            else:
                st.error("❌ Likely Declined")

            requests_session.post(
                f"{API_BASE_URL}/update_settings",
                params={"store_data": st.session_state.get("store_data", "Yes") == "Yes"}
            )
            requests_session.post(f"{API_BASE_URL}/store_user_data", json=input_payload)

            explain_response = requests_session.post(f"{API_BASE_URL}/explain", json=input_payload)
            explanation = pd.Series(explain_response.json())

            st.markdown("#### 🔍 Decision Factors")
            plt = plot_feature_importance(explanation)
            st.pyplot(plt)
            
            
            st.session_state["show_feedback"] = True

    if st.session_state.get("show_application") == 0 and st.session_state.get("application_data"):
        show_credit_form(st.session_state["application_data"])
    elif st.session_state.get("show_application") == 1:
        st.success("Thank you! Manager will contact you soon!")

    if st.session_state.get("show_feedback") == 1 and st.session_state.get("application_data"):
        show_feedback_form(st.session_state["application_data"])
    if st.session_state.get("show_feedback") == 2:
        st.success("Thank you! We'll review your feedback.")
