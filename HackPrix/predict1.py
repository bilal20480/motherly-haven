import streamlit as st
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from google import generativeai as genai

# -------------------- Gemini API Setup --------------------
GEMINI_API_KEY = "AIzaSyCnIkKmtRYHwJOMGGa244-XdWXYtIR_RwE"  # replace this with your actual key
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

# -------------------- Page Setup --------------------
st.set_page_config(page_title="Postpartum Mental Health Checker", layout="centered")
st.title("🤱 Postpartum Mental Health Prediction ")

# -------------------- Load and Train --------------------
@st.cache_data
def load_and_train():
    df = pd.read_csv("postpartum_mental_health_dataset_named.csv")
    X = df.iloc[:, 0:10]
    y_ppd = df["Postpartum_Depression"]
    y_anx = df["Postpartum_Anxiety"]
    y_psy = df["Postpartum_Psychosis"]

    X_train, _, y_ppd_train, _ = train_test_split(X, y_ppd, test_size=0.2, random_state=42)
    _, _, y_anx_train, _ = train_test_split(X, y_anx, test_size=0.2, random_state=42)
    _, _, y_psy_train, _ = train_test_split(X, y_psy, test_size=0.2, random_state=42)

    model_ppd = RandomForestClassifier(n_estimators=100, random_state=42).fit(X_train, y_ppd_train)
    model_anx = RandomForestClassifier(n_estimators=100, random_state=42).fit(X_train, y_anx_train)
    model_psy = RandomForestClassifier(n_estimators=100, random_state=42).fit(X_train, y_psy_train)

    return model_ppd, model_anx, model_psy, X.columns.tolist()

model_ppd, model_anx, model_psy, features = load_and_train()

# -------------------- Input Form --------------------
questions = [
    "Have you felt sad or down recently?",
    "Do you feel overwhelmed caring for your baby?",
    "Do you experience panic, fear, or frequent worry?",
    "Do you have trouble sleeping even when your baby sleeps?",
    "Have you lost interest in things you usually enjoy?",
    "Do you feel disconnected from your baby?",
    "Do you see or hear things that others don’t?",
    "Do you feel someone is watching or plotting against you?",
    "Have you had thoughts of harming yourself?",
    "Have you had thoughts of harming your baby?"
]
options = ["Not at all", "Sometimes", "Often", "Almost always"]
option_scores = {"Not at all": 0, "Sometimes": 1, "Often": 2, "Almost always": 3}

st.markdown("### 📝 Please answer the following:")
user_input = [option_scores[st.selectbox(q, options, key=f"q{i}")] for i, q in enumerate(questions)]

# -------------------- Prediction --------------------
if st.button("🔍 Predict"):
    input_df = pd.DataFrame([user_input], columns=features)

    pred_ppd = model_ppd.predict(input_df)[0]
    pred_anx = model_anx.predict(input_df)[0]
    pred_psy = model_psy.predict(input_df)[0]

    diagnosis = []
    if pred_ppd: diagnosis.append("Postpartum Depression")
    if pred_anx: diagnosis.append("Postpartum Anxiety")
    if pred_psy: diagnosis.append("Postpartum Psychosis")

    # Display result
    st.subheader("🔎 Prediction Result:")
    if diagnosis:
        st.error(f"⚠️ Detected: {', '.join(diagnosis)}")
    else:
        st.success("✅ No major symptoms detected.")

    # -------------------- Gemini Recommendation --------------------
    with st.spinner("🧠 Thinking with Gemini..."):
        prompt = f"""
        A postpartum mother is showing symptoms of: {', '.join(diagnosis) if diagnosis else "None"}.
        Please provide friendly, non-clinical advice and emotional support that she can follow.
        Also suggest when she should consult a professional.
        it should be of 150 words only and in bullet points
        """

        gemini_response = model.generate_content(prompt)
        st.markdown("### Suggestions based on the condition:")
        st.write(gemini_response.text)
