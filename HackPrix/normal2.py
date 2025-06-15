import streamlit as st
import speech_recognition as sr
import pyttsx3
import google.generativeai as genai
import nltk

# Configure Gemini API
genai.configure(api_key="AIzaSyC9jEg8Icw6kMPs0tdncQKUCGtdeI_xINo")  # Replace with your Gemini key

nltk.download("punkt")

# --- TTS Function ---
def speak_text(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

# --- STT Function ---
def speech_to_text():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)
        speak_text("Please describe your response.")
        audio = recognizer.listen(source, timeout=5, phrase_time_limit=8)

    try:
        text = recognizer.recognize_google(audio)
        return text
    except sr.UnknownValueError:
        speak_text("Sorry, I didn’t catch that.")
        return ""
    except sr.RequestError:
        speak_text("There was an issue with the speech service.")
        return ""

# --- Gemini Classification ---
def classify_condition(trimester, full_input):
    model = genai.GenerativeModel("gemini-1.5-flash")
    prompt = f"""
A pregnant woman in her {trimester} trimester described the following:

\"\"\"{full_input}\"\"\"

Please classify her condition as either:
- "normal": if the situation seems okay and not immediately concerning.
- "risky": if there's any sign of danger or unusual behavior that needs medical attention.

💬 Response format:
- Start with *"normal"* or *"risky"*.
- Follow it with a short, heartwarming explanation suitable for a non-medical person.
- Use gentle, kind tone like you're talking to someone you care about deeply.

Example:
normal – Don’t worry, gentle back pain and fatigue are quite common in early pregnancy. You're doing well!

OR

risky – It’s okay to be concerned. These symptoms may require a doctor’s help. You’re not alone—please seek support.

Reply only in this format.
"""
    response = model.generate_content(prompt)
    reply = response.text.strip().lower()

    if reply.startswith("normal"):
        return "normal", reply
    elif reply.startswith("risky"):
        return "risky", reply
    else:
        return "unknown", reply

# --- Streamlit App ---
st.set_page_config(page_title="Pregnancy Symptom Checker", layout="centered")
st.title("🤱 Pregnancy Health Voice Checker")

st.markdown("Use your voice to describe what you're going through, and we'll help understand if it's normal or needs attention. 💖")

# --- Basic Info ---
st.subheader("👩‍⚕ Patient Information")
name = st.text_input("Full Name")
age = st.number_input("Age", min_value=15, max_value=50, step=1)
weeks = st.number_input("Weeks Pregnant", min_value=1, max_value=42, step=1)

trimester = ""
responses = []

if weeks <= 13:
    trimester = "first"
elif 14 <= weeks <= 27:
    trimester = "second"
else:
    trimester = "third"

st.write(f"Detected Trimester: *{trimester.capitalize()} Trimester*")

# --- Start Check ---
if st.button("🎙 Start Voice Health Check"):

    # Questions per trimester
    trimester_questions = {
        "first": [
            "Are you feeling symptoms like nausea, vomiting, or spotting?",
            "Does the pain get worse when sitting, walking, or doing work?",
            "How would you describe the discomfort—mild, sharp, or unusual?"
        ],
        "second": [
            "Do you feel pressure or cramping in your lower abdomen or back?",
            "Is the pain affecting your daily activities or sleep?",
            "Can you tell how the pain feels—tight, pulling, or heavy?"
        ],
        "third": [
            "Do you feel tightness, contractions, or water leakage?",
            "Is the pain frequent and does it increase when you move or rest?",
            "Does this feel like something new or have you felt it before?"
        ]
    }

    for idx, question in enumerate(trimester_questions[trimester], 1):
        speak_text(f"Question {idx}. {question}")
        user_input = speech_to_text()
        responses.append(f"Q{idx}: {user_input}")
        st.write(f"*Q{idx} Response:*", user_input)

    # Join responses for analysis
    full_conversation = " ".join(responses)

    # --- Classification ---
    st.subheader("🧠 Final Health Assessment")
    classification, explanation = classify_condition(trimester, full_conversation)

    if classification == "risky":
        speak_text("This may be risky. Please talk to your doctor.")
        st.error("⚠ Risky condition detected.\n\n" + explanation)
    elif classification == "normal":
        speak_text("This appears to be normal. Keep taking care.")
        st.success("✅ Everything seems normal.\n\n" + explanation)
    else:
        speak_text("I'm not sure. Please try again or ask your doctor.")
        st.warning("⚠ Unable to classify.\n\n" + explanation)