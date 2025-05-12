import streamlit as st

def greetings_page():
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
    # st.image("https://via.placeholder.com/800x400.png?text=Credit+Scoring+App", use_container_width=True)

    # Add a "Get Started" button
    if st.button("Get Started"):
        st.session_state["page"] = "settings"
        st.rerun()