import streamlit as st

def greetings_page():
    st.markdown("""
    <style>
        .welcome-header {
            color: #2c3e50 !important;
            text-align: center;
        }
        .feature-card {
            background-color: #f8f9fa !important;
            padding: 20px;
            border-radius: 10px;
            margin-bottom: 20px;
        }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown('<h1 class="welcome-header">Welcome to the Credit Scoring App</h1>', unsafe_allow_html=True)
    st.title("Welcome to the Credit Scoring App")
    st.markdown("""
    ## Why do we help?
    This application is designed to assist users in evaluating their credit approval chances using an AI-powered model. 
    The model provides predictions and explanations for the factors influencing the decision.

    ## Ethics & Security
    - The model's predictions are **not final** and do not influence the actual credit decision.
    - All users are treated fairly, and no sensitive or discriminatory data is used in the model.
    - The purpose of this tool is to provide transparency and assist users in understanding their financial profile.
    - We **will not** store your data if you don't want. 
    - If you agree to share your data we will ananymize and store it securly. 

    After receiving the model's prediction, you can contact a manager to discuss your credit options. The final decision is made by the manager, not the model.
    """)
    
    # Добавляем key к кнопке
    if st.button("Get Started", key="greetings_get_started_btn"):
        st.session_state["page"] = "consent"
        st.rerun()