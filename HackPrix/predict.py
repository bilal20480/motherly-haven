import streamlit as st
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

st.set_page_config(page_title="Postpartum Mental Health Checker", layout="centered")
st.title("🤱 Postpartum Mental Health Prediction")

# Load dataset
@st.cache_data
def load_data():
    df = pd.read_csv("postpartum_mental_health_dataset_named.csv")
    return df

df = load_data()

# Features and labels
X = df.iloc[:, 0:10]
y_ppd = df["Postpartum_Depression"]
y_anx = df["Postpartum_Anxiety"]
y_psy = df["Postpartum_Psychosis"]

# Train models
def train_models(X, y_ppd, y_anx, y_psy):
    X_train, X_test, y_ppd_train, y_ppd_test = train_test_split(X, y_ppd, test_size=0.2, random_state=42)
    _, _, y_anx_train, y_anx_test = train_test_split(X, y_anx, test_size=0.2, random_state=42)
    _, _, y_psy_train, y_psy_test = train_test_split(X, y_psy, test_size=0.2, random_state=42)

    model_ppd = RandomForestClassifier(n_estimators=100, random_state=42)
    model_ppd.fit(X_train, y_ppd_train)

    model_anx = RandomForestClassifier(n_estimators=100, random_state=42)
    model_anx.fit(X_train, y_anx_train)

    model_psy = RandomForestClassifier(n_estimators=100, random_state=42)
    model_psy.fit(X_train, y_psy_train)

    return model_ppd, model_anx, model_psy

model_ppd, model_anx, model_psy = train_models(X, y_ppd, y_anx, y_psy)

# Input questions
st.markdown("### 📝 Please answer the following based on your feelings recently:")
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

user_input = []
for i, q in enumerate(questions):
    selected = st.selectbox(f"Q{i+1}. {q}", options, key=f"q{i}")
    user_input.append(option_scores[selected])

# Prediction
if st.button("🔍 Predict My Mental Health"):
    input_df = pd.DataFrame([user_input], columns=X.columns)
    pred_ppd = model_ppd.predict(input_df)[0]
    pred_anx = model_anx.predict(input_df)[0]
    pred_psy = model_psy.predict(input_df)[0]

    st.subheader("🔎 Prediction Result:")

    if pred_ppd:
        st.error("⚠️ You may be experiencing **Postpartum Depression (PPD)**.")
    else:
        st.success("✅ No significant signs of PPD detected.")

    if pred_anx:
        st.warning("⚠️ Signs of **Postpartum Anxiety** detected.")
    else:
        st.success("✅ No significant signs of anxiety.")

    if pred_psy:
        st.error("🚨 Possible **Postpartum Psychosis**. Please seek immediate help.")
    else:
        st.success("✅ No significant signs of psychosis.")

    st.markdown("---")
    st.info("📌 This result is not a diagnosis. Please consult a professional if you have any concerns.")
