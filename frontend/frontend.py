import streamlit as st
import pandas as pd
import requests
import matplotlib.pyplot as plt
import seaborn as sns
from greetings import greetings_page

# Constants and settings
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

# Page settings
st.set_page_config(
    page_title="Credit Scoring System",
    page_icon="🏠",
    layout="wide"
)

def plot_feature_importance(importances):
    """Feature importance visualization with seamless Streamlit integration"""
    # Color scheme matching Streamlit's theme
    BG_COLOR = "#f0f2f6"  # Streamlit's background color
    TEXT_COLOR = "#262730"  # Text color
    POS_COLOR = "#21c354"  # Green for positive impact
    NEG_COLOR = "#ff2b2b"  # Red for negative impact
    GRID_COLOR = "#d0d0d7"  # Grid lines color
    BAR_EDGE = "#e6e9ef"    # Bar edge color

    # Create figure with correct background settings
    plt.style.use('default')
    fig = plt.figure(figsize=(10, 6), facecolor=BG_COLOR, dpi=100)
    ax = fig.add_subplot(facecolor=BG_COLOR)

    # Human-readable feature names
    feature_names = {
        'amt_income_total': 'Annual Income',
        'code_income_type': 'Income Type',
        'code_education_type': 'Education',
        'age_group': 'Age Group',
        'years_employed_cat': 'Employment Duration',
        'cnt_family_members': 'Family Members',
        'cnt_children': 'Number of Children',
        'flag_own_realty': 'Owns Property',
        'flag_own_car': 'Owns Car',
        'code_family_status': 'Marital Status',
        'code_housing_type': 'Housing Type',
        'code_occupation_type': 'Occupation'
    }

    # Prepare dataframe
    df = pd.DataFrame({
        'Factor': [feature_names.get(col, col) for col in importances.index],
        'Impact': importances.values,
        'Effect': ['Increases' if x > 0 else 'Decreases' for x in importances.values]
    }).sort_values('Impact', key=abs, ascending=False)

    # Create the bar plot
    sns.barplot(
        data=df,
        x='Impact',
        y='Factor',
        hue='Effect',
        palette={'Increases': POS_COLOR, 'Decreases': NEG_COLOR},
        ax=ax,
        dodge=False,
        linewidth=0.5,
        edgecolor=BAR_EDGE
    )

    # Styling
    ax.set_title('Key Decision Factors', 
                pad=20, fontsize=14, color=TEXT_COLOR, fontweight='bold')
    ax.set_xlabel('Impact Score', fontsize=12, color=TEXT_COLOR)
    ax.set_ylabel('')  # Remove y-label as factors are self-explanatory

    # Customize ticks and spines
    ax.tick_params(axis='both', colors=TEXT_COLOR)
    for spine in ax.spines.values():
        spine.set_color(GRID_COLOR)

    # Add zero line and grid
    ax.axvline(0, color=TEXT_COLOR, linestyle='--', linewidth=0.8, alpha=0.7)
    ax.grid(axis='x', color=GRID_COLOR, linestyle=':', linewidth=0.5, alpha=0.6)

    # Legend styling
    legend = ax.legend(
        title='Impact Direction',
        facecolor=BG_COLOR,
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
                        "name": name,
                        "email": email,
                        "type": feedback_type,
                        "details": feedback_details,
                        "application_data": user_data if user_data else None
                    }
                    
                    response = requests_session.post(
                        f"{API_BASE_URL}/submit_feedback",
                        json=feedback_data
                    )
                    
                    if response.status_code == 200:
                        st.success("Thank you! We'll review your feedback.")
                    else:
                        st.error("Submission failed. Please try later.")
                except Exception as e:
                    st.error(f"Connection error: {str(e)}")

# Main app logic
if "page" not in st.session_state:
    st.session_state["page"] = "greetings"
    st.session_state["show_feedback"] = False
    st.session_state["application_data"] = None

if st.session_state["page"] == "greetings":
    greetings_page()
elif st.session_state["page"] == "main":
    # Header with Home button
    col1, col2 = st.columns([1, 10])
    with col1:
        if st.button("🏠 Home"):
            st.session_state["page"] = "greetings"
            st.rerun()
    with col2:
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
            code_gender = st.selectbox("Gender", options=[0, 1], format_func=lambda x: "Male" if x == 1 else "Female")
            flag_own_car = st.selectbox("Owns a Car", options=[0, 1], format_func=lambda x: "Yes" if x == 1 else "No")
            flag_own_realty = st.selectbox("Owns Property", options=[0, 1], format_func=lambda x: "Yes" if x == 1 else "No")
            cnt_children = st.number_input("Number of Children", min_value=0, value=0)
            amt_income_total = st.number_input("Annual Income ($)", min_value=0, value=50000)

        with col2:
            email = st.text_input("Email")
            code_income_type = st.selectbox("Income Type", options=list(INCOME_TYPES.keys()))
            code_education_type = st.selectbox("Education Level", options=list(EDUCATION_TYPES.keys()))
            code_family_status = st.selectbox("Marital Status", options=list(FAMILY_STATUSES.keys()))
            code_housing_type = st.selectbox("Housing Type", options=list(HOUSING_TYPES.keys()))
            cnt_family_members = st.number_input("Family Members", min_value=1, value=1)

        age_group = st.selectbox("Age Group", options=list(AGE_GROUPS.keys()), format_func=lambda x: AGE_GROUPS[x])
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

            requests_session.post(f"{API_BASE_URL}/store_user_data", json=input_payload)

            explain_response = requests_session.post(f"{API_BASE_URL}/explain", json=input_payload)
            explanation = pd.Series(explain_response.json())

            st.markdown("#### 🔍 Decision Factors")
            plt = plot_feature_importance(explanation)
            st.pyplot(plt)
            
            st.markdown("""
            <div style="background-color:#f8f9fa; padding:10px; border-radius:5px; margin-top:10px">
            <small>
            <b>How to read:</b> Factors sorted by impact strength.<br>
            Green - increases approval chance, Red - decreases.
            </small>
            </div>
            """, unsafe_allow_html=True)
            
            st.session_state["show_feedback"] = True

    # Feedback form
    if st.session_state.get("show_feedback") and st.session_state.get("application_data"):
        show_feedback_form(st.session_state["application_data"])
        
        if st.button("← Back to Results"):
            st.session_state["show_feedback"] = False
            st.rerun()