
import streamlit as st
import pandas as pd
import joblib
import json
import os
from datetime import datetime
from features_extraction import extract_features

# ==========================================
# PAGE CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="AI PASSWORD STRENGTH ANALYZER",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================
# LOAD MODEL AND METRICS
# ==========================================

@st.cache_resource
def load_model():
    if os.path.exists("password_model.pkl"):
        return joblib.load("password_model.pkl")
    return None

@st.cache_data
def load_metrics():
    if os.path.exists("model_metrics.json"):
        with open("model_metrics.json", "r") as f:
            return json.load(f)
    return {}

model = load_model()
metrics = load_metrics()

# ==========================================
# CYBERPUNK WALLPAPER AND CSS
# ==========================================

st.html("""
<style>

/* BACKGROUND */
.stApp {
    background: #050510 !important;
    position: relative;
}

/* CYBERPUNK CITY GLOW */
.stApp::before {
    content: "";
    position: fixed;
    inset: 0;
    z-index: 0;
    pointer-events: none;
    background:
        radial-gradient(ellipse at 15% 80%, rgba(0,180,255,.25), transparent 35%),
        radial-gradient(ellipse at 85% 70%, rgba(180,0,255,.22), transparent 38%),
        repeating-linear-gradient(
            90deg,
            transparent 0px,
            transparent 55px,
            rgba(0,225,255,.08) 56px,
            transparent 58px
        ),
        linear-gradient(180deg,#08091e,#10102b 55%,#050510);
    animation: cityGlow 8s ease-in-out infinite alternate;
}

/* ANIMATED RAIN */
.stApp::after {
    content: "";
    position: fixed;
    inset: 0;
    z-index: 0;
    pointer-events: none;
    background-image: repeating-linear-gradient(
        105deg,
        transparent 0px,
        transparent 18px,
        rgba(120,220,255,.18) 19px,
        transparent 20px,
        transparent 38px
    );
    background-size: 100px 180px;
    animation: rainFall .65s linear infinite;
    opacity: .35;
}

/* CONTENT LAYERS */
[data-testid="stAppViewContainer"] {
    background: transparent !important;
    position: relative;
}

[data-testid="stMain"] {
    background: transparent !important;
    position: relative;
    z-index: 2;
}

[data-testid="stMainBlockContainer"] {
    position: relative;
    z-index: 3;
    max-width: 1500px !important;
    padding: 2rem 3rem !important;
}

/* SIDEBAR */
[data-testid="stSidebar"] {
    background: rgba(5,7,24,.94) !important;
    border-right: 1px solid rgba(0,225,255,.4);
    position: relative;
    z-index: 4;
}

[data-testid="stSidebar"] * {
    color: #e5f7ff;
}

/* MAIN TITLE */
.sentinel-title {
    font-size: clamp(38px,5vw,66px);
    font-weight: 900;
    letter-spacing: 5px;
    text-align: center;
    color: #00eaff;
    text-shadow:
        0 0 8px #00eaff,
        0 0 20px #0077ff,
        0 0 40px #0077ff;
    margin-bottom: 0;
}

.sentinel-subtitle {
    text-align: center;
    color: #c5c9ff;
    letter-spacing: 4px;
    font-size: 13px;
    margin: 5px 0 35px;
}

/* HEADINGS AND TEXT */
h1,h2,h3 {
    color: #e8faff !important;
    text-shadow: 0 0 12px rgba(0,225,255,.2);
}

p, label, li {
    color: #e1e9ff;
}

/* METRIC CARDS */
[data-testid="stMetric"] {
    min-height: 115px;
    background: rgba(8,15,45,.82) !important;
    border: 1px solid rgba(0,234,255,.5) !important;
    border-radius: 16px !important;
    padding: 16px !important;
    overflow-wrap: anywhere;
    box-shadow: 0 0 18px rgba(0,180,255,.1);
}

[data-testid="stMetricLabel"] {
    font-size: 14px !important;
}

[data-testid="stMetricValue"] {
    font-size: 25px !important;
}

/* CONTAINERS */
[data-testid="stVerticalBlockBorderWrapper"] {
    background: rgba(8,12,35,.72) !important;
    border: 1px solid rgba(0,225,255,.25);
    border-radius: 14px;
    backdrop-filter: blur(8px);
}

/* INPUTS */
.stTextInput input,
.stTextArea textarea {
    background: rgba(7,10,30,.95) !important;
    color: white !important;
    border: 1px solid rgba(0,225,255,.5) !important;
    border-radius: 9px !important;
}

/* BUTTONS */
.stButton button,
.stDownloadButton button {
    background: linear-gradient(100deg,#006eff,#8b2cff);
    color: white !important;
    border: 1px solid #00eaff;
    border-radius: 9px;
    font-weight: 800;
    transition: .25s ease;
}

.stButton button:hover,
.stDownloadButton button:hover {
    box-shadow: 0 0 18px #00d9ff;
    transform: translateY(-2px);
}

/* ANIMATIONS */
@keyframes rainFall {
    from { background-position: 0 0; }
    to { background-position: 0 180px; }
}

@keyframes cityGlow {
    from { filter: brightness(.78); }
    to { filter: brightness(1.15); }
}

/* FOOTER */
.sentinel-footer {
    text-align: center;
    color: #8996c7;
    font-size: 12px;
    letter-spacing: 2px;
    padding: 25px 0 10px;
    border-top: 1px solid rgba(0,225,255,.2);
    margin-top: 40px;
}

</style>
""")

# ==========================================
# HEADER
# ==========================================

st.markdown("""
<div class="sentinel-title">PASSWORD STRENGTH CHECKER</div>
<div class="sentinel-subtitle">
AI-BASED PASSWORD STRENGTH CHECKER USING MACHINE LEARNING
</div>
""", unsafe_allow_html=True)

# ==========================================
# SIDEBAR
# ==========================================

st.sidebar.markdown("## 🔐 PASSWORD STRENGTH CHECKER")
st.sidebar.caption("AI-BASED MACHINE LEARNING PROJECT")

page = st.sidebar.radio(
    "NAVIGATION",
    [
        "Dashboard",
        "Password Analyzer",
        "Model Analytics",
        "About Project",
        "Project Team"
    ]
)

st.sidebar.divider()
st.sidebar.caption("SYSTEM STATUS")

if model is not None:
    st.sidebar.success("ML Model Loaded")
else:
    st.sidebar.error("Model Not Found")

st.sidebar.caption("Version 1.0 | SENTINEL AI")

# ==========================================
# HELPER FUNCTIONS
# ==========================================

def normalized_accuracy(value):
    value = float(value)
    return value / 100 if value > 1 else value

def get_password_score(features):
    score = 0

    if features.get("length", 0) >= 12:
        score += 25
    elif features.get("length", 0) >= 8:
        score += 15

    if features.get("has_uppercase"):
        score += 15
    if features.get("has_lowercase"):
        score += 10
    if features.get("has_digit"):
        score += 15
    if features.get("has_special"):
        score += 20
    if not features.get("has_repeated_chars"):
        score += 10
    if not features.get("has_sequence"):
        score += 5

    return min(score, 100)

def analyze_password(password):
    if not password:
        st.warning("Enter a fictional test password.")
        return

    if model is None:
        st.error("Model not found. Run train_model.py first.")
        return

    features = extract_features(password)
    feature_df = pd.DataFrame([features])

    prediction = model.predict(feature_df)[0]

    confidence = None
    if hasattr(model, "predict_proba"):
        confidence = float(max(model.predict_proba(feature_df)[0])) * 100

    score = get_password_score(features)

    st.divider()
    st.subheader("Analysis Results")

    c1,c2,c3 = st.columns(3)

    with c1:
        st.metric("ML Prediction", str(prediction).upper())

    with c2:
        st.metric("Illustrative Score", f"{score}/100")

    with c3:
        st.metric(
            "Model Confidence",
            f"{confidence:.1f}%" if confidence is not None else "N/A"
        )

    if str(prediction).lower() == "strong":
        st.success("Strong classification by the trained model.")
    elif str(prediction).lower() == "medium":
        st.warning("Medium classification by the trained model.")
    else:
        st.error("Weak classification by the trained model.")

    st.subheader("Feature Analysis")

    items = [
        ("Length", features.get("length", 0)),
        ("Uppercase", features.get("uppercase_count", 0)),
        ("Lowercase", features.get("lowercase_count", 0)),
        ("Digits", features.get("digit_count", 0)),
        ("Special Characters", features.get("special_count", 0)),
        ("Repeated Characters", "Yes" if features.get("has_repeated_chars") else "No"),
        ("Sequence Detected", "Yes" if features.get("has_sequence") else "No")
    ]

    columns = st.columns(3)

    for i,(name,value) in enumerate(items):
        with columns[i % 3]:
            st.metric(name, value)

    st.subheader("Recommendations")

    recommendations = []

    if features.get("length",0) < 12:
        recommendations.append("Use a longer password.")
    if not features.get("has_uppercase"):
        recommendations.append("Include uppercase letters.")
    if not features.get("has_lowercase"):
        recommendations.append("Include lowercase letters.")
    if not features.get("has_digit"):
        recommendations.append("Include numbers.")
    if not features.get("has_special"):
        recommendations.append("Include special characters.")
    if features.get("has_repeated_chars"):
        recommendations.append("Avoid repeated characters.")
    if features.get("has_sequence"):
        recommendations.append("Avoid predictable sequences.")

    if recommendations:
        for item in recommendations:
            st.write("•",item)
    else:
        st.success("No basic feature recommendations.")

    report = {
        "project": "SENTINEL AI",
        "prediction": str(prediction),
        "illustrative_score": score,
        "model_confidence": confidence,
        "features": features,
        "recommendations": recommendations,
        "generated_at": datetime.now().isoformat()
    }

    st.download_button(
        "⬇️ Download Analysis Report",
        data=json.dumps(report,indent=4),
        file_name="sentinel_password_report.json",
        mime="application/json"
    )

    st.caption(
        "Educational demonstration only. The score and prediction do not "
        "guarantee real-world password security. Never enter a personal "
        "or currently used password."
    )

# ==========================================
# DASHBOARD
# ==========================================

if page == "Dashboard":

    st.title("⚡ Security Dashboard")
    st.write(
        "Welcome to SENTINEL AI — AI-Based Password Strength Checker."
    )

    st.subheader("System Overview")

    c1,c2,c3,c4 = st.columns(4)

    with c1:
        st.metric("ML Algorithm","Random Forest")

    with c2:
        st.metric("Features","11")

    with c3:
        st.metric("Training Samples",f"{metrics.get('total_samples',10000):,}")

    with c4:
        accuracy = metrics.get("accuracy")
        if accuracy is not None:
            st.metric(
                "Test Accuracy",
                f"{normalized_accuracy(accuracy)*100:.2f}%"
            )
        else:
            st.metric("Test Accuracy","N/A")

    st.divider()
    st.subheader("Core Capabilities")

    left,right = st.columns(2)

    with left:
        st.markdown("### 🧠 Machine Learning")
        st.write(
            "Uses a Random Forest classification model to categorize "
            "fictional test passwords into Weak, Medium, or Strong."
        )

        st.markdown("### 🔍 Feature Extraction")
        st.write(
            "Analyzes password length, character variety, repeated "
            "characters, and simple sequences."
        )

    with right:
        st.markdown("### 📊 Model Analytics")
        st.write(
            "Displays training metrics, class distribution, confusion "
            "matrix, and classification report."
        )

        st.markdown("### 📄 Report Generation")
        st.write(
            "Exports password analysis results as a downloadable JSON report."
        )

    st.divider()
    st.info(
        "Use the Password Analyzer page to test fictional sample passwords."
    )

# ==========================================
# PASSWORD ANALYZER
# ==========================================

elif page == "Password Analyzer":

    st.title("🔐 Password Analyzer")
    st.write(
        "Analyze a fictional sample password using the trained ML model."
    )

    st.warning(
        "Do not enter your real password or any password you currently use."
    )

    password = st.text_input(
        "Enter a fictional test password",
        type="password",
        placeholder="Example: Demo#4821Sample"
    )

    if st.button("🚀 ANALYZE PASSWORD",use_container_width=True):
        analyze_password(password)

# ==========================================
# MODEL ANALYTICS
# ==========================================

elif page == "Model Analytics":

    st.title("📊 Model Analytics")

    if not metrics:
        st.error("Metrics file not found. Run train_model.py first.")
    else:
        accuracy = metrics.get("accuracy")
        total_samples = metrics.get("total_samples",10000)
        feature_count = metrics.get("feature_count",11)

        c1,c2,c3 = st.columns(3)

        with c1:
            if accuracy is not None:
                st.metric(
                    "Test Accuracy",
                    f"{normalized_accuracy(accuracy)*100:.2f}%"
                )

        with c2:
            st.metric("Dataset Size",f"{total_samples:,}")

        with c3:
            st.metric("Features Used",feature_count)

        st.divider()
        st.subheader("Dataset Distribution")

        distribution = metrics.get("class_distribution")

        if isinstance(distribution,dict):
            df = pd.DataFrame(
                list(distribution.items()),
                columns=["Class","Samples"]
            )
            st.bar_chart(df.set_index("Class"))

        st.subheader("Confusion Matrix")

        matrix = metrics.get("confusion_matrix")

        if matrix:
            labels = metrics.get(
                "labels",
                ["Weak","Medium","Strong"]
            )
            matrix_df = pd.DataFrame(
                matrix,
                index=labels,
                columns=labels
            )
            st.dataframe(matrix_df,use_container_width=True)

        st.subheader("Classification Report")

        report = metrics.get("classification_report")

        if isinstance(report,dict):
            report_df = pd.DataFrame(report).transpose()
            st.dataframe(report_df,use_container_width=True)

        st.divider()
        st.subheader("Model Configuration")
        st.write("Algorithm: Random Forest Classifier")
        st.write("Number of estimators: 200")
        st.write("Maximum depth: 12")
        st.write("Random state: 42")

        st.caption(
            "Accuracy is measured against synthetic labels generated "
            "by project rules. It is not independently verified "
            "real-world password security performance."
        )

# ==========================================
# ABOUT PROJECT
# ==========================================

elif page == "About Project":

    st.title("📘 About SENTINEL AI")

    st.markdown("""
    ### AI-Based Password Strength Checker Using Machine Learning

    SENTINEL AI is an academic project demonstrating how machine
    learning can classify password patterns.

    ### Project Objectives

    - Extract meaningful features from sample passwords.
    - Train a Random Forest classification model.
    - Classify passwords into Weak, Medium, and Strong categories.
    - Display model evaluation metrics.
    - Generate downloadable analysis reports.

    ### Technologies Used

    - Python
    - Streamlit
    - Pandas
    - Scikit-learn
    - Joblib
    - Machine Learning

    ### Machine Learning Workflow

    1. Generate a synthetic dataset.
    2. Extract password features.
    3. Assign labels using project rules.
    4. Train the Random Forest model.
    5. Evaluate the model.
    6. Use the trained model in the Streamlit application.
    """)

    st.info(
        "This is an educational prototype, not a professional password "
        "auditing or security certification tool."
    )

# ==========================================
# PROJECT TEAM
# ==========================================

elif page == "Project Team":

    st.title("👨‍💻 Project Team")
    st.write("SAPTHAGIRI NPS UNIVERSITY")
    st.write("Department of CSE-AIML")

    team = [
        ("Sandesh M K","25SUUBEAML540"),
        ("Sandesh M J","25SUUBEAML541"),
        ("Sange Tsering","25SUUBEAML542"),
        ("Sonthosh R M","25SUUBEAML560"),
        ("Sanjay K","25SUUBEAML555")
    ]

    for name,srn in team:
        with st.container(border=True):
            c1,c2 = st.columns([2,1])
            with c1:
                st.subheader(name)
            with c2:
                st.write(f"SRN: {srn}")

    st.divider()

    st.markdown("""
    ### Project Information

    **Project:** SENTINEL AI

    **Domain:** Artificial Intelligence and Machine Learning

    **Department:** CSE-AIML

    **University:** SAPTHAGIRI NPS UNIVERSITY
    """)

# ==========================================
# FOOTER
# ==========================================

st.markdown("""
<div class="sentinel-footer">
SENTINEL AI | INTELLIGENT PASSWORD SECURITY
<br><br>
SAPTHAGIRI NPS UNIVERSITY • CSE-AIML
</div>
""",unsafe_allow_html=True)
