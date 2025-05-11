import streamlit as st

def greetings_page():
    st.markdown("""
    <style>
        .welcome-container {
            background-color: #ffffff;
            padding: 2rem;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            margin-bottom: 2rem;
        }
        .welcome-header {
            color: #2c3e50;
            text-align: center;
            margin-bottom: 1.5rem;
        }
        .feature-card {
            background-color: #f8f9fa;
            padding: 1.5rem;
            border-radius: 10px;
            margin-bottom: 1rem;
            border-left: 4px solid #3498db;
        }
        .ethics-section {
            background-color: #f8f9fa;
            padding: 1.5rem;
            border-radius: 10px;
            margin-top: 1.5rem;
        }
    </style>
    """, unsafe_allow_html=True)

    st.markdown('<div class="welcome-container">', unsafe_allow_html=True)
    st.markdown('<h1 class="welcome-header">Welcome to the Credit Scoring App</h1>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="feature-card">
        <h3>Why use our service?</h3>
        <p>Get instant credit approval predictions with transparent explanations of the factors influencing the decision.</p>
    </div>
    """, unsafe_allow_html=True)

    cols = st.columns(3)
    features = [
        ("⚡ Fast", "Get results in seconds"),
        ("🔍 Transparent", "Understand why decisions are made"),
        ("🛡️ Secure", "Your data is protected")
    ]
    
    for i, (icon, text) in enumerate(features):
        with cols[i]:
            st.markdown(f"""
            <div class="feature-card">
                <h4>{icon}</h4>
                <p>{text}</p>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("""
    <div class="ethics-section">
        <h3>Our Principles</h3>
        <ul>
            <li><strong>Fairness:</strong> The model is regularly audited for bias</li>
            <li><strong>Transparency:</strong> Clear explanations of all decisions</li>
            <li><strong>Privacy:</strong> You control your data</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

    if st.button("Get Started", key="greetings_get_started_btn"):
        st.session_state["page"] = "consent"
        st.rerun()