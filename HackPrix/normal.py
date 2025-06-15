import streamlit as st
import speech_recognition as sr
import pyttsx3
import google.generativeai as genai
import nltk
from datetime import datetime

# Set your Gemini API Key
genai.configure(api_key="AIzaSyC9jEg8Icw6kMPs0tdncQKUCGtdeI_xINo")  # Replace with your actual Gemini key

# Download necessary NLTK data
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
        speak_text("Please describe your issue.")
        audio = recognizer.listen(source)

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
def classify_condition(full_input):
    model = genai.GenerativeModel("gemini-1.5-flash")
    prompt = f"""
A pregnant woman described her symptoms and answered a few questions:

\"\"\"{full_input}\"\"\"

Please classify her condition as either:
- "normal": if the situation seems okay and not immediately concerning.
- "risky": if there is any sign of danger or unusual behavior that needs medical attention.

🧠 Format:
Start your response with the word "normal" or "risky", followed by a brief, 1–2 sentence explanation suitable for a non-medical person.

Example:
normal – Mild back pain and tiredness are typical during pregnancy and not usually serious.

OR

risky – Heavy bleeding or severe cramping should be evaluated by a doctor immediately.

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
st.title("🤰 Is This Normal? – Pregnancy Symptom Checker")

st.markdown("This app uses speech and AI to help identify if a pregnancy-related symptom is *normal* or *risky*. Please speak clearly into the microphone.")

if st.button("🎙️ Start Health Check"):
    responses = []

    # Question 1
    speak_text("Describe the problem you're facing.")
    q1 = speech_to_text()
    responses.append(f"Problem Description: {q1}")
    st.write("**Q1 Response:**", q1)

    # Question 2
    speak_text("How long have you been feeling this way?")
    q2 = speech_to_text()
    responses.append(f"Duration: {q2}")
    st.write("**Q2 Response:**", q2)

    # Question 3
    speak_text("Is the symptom getting better, worse, or staying the same?")
    q3 = speech_to_text()
    responses.append(f"Change in condition: {q3}")
    st.write("**Q3 Response:**", q3)

    full_conversation = " ".join(responses)

    # Classification
    classification, explanation = classify_condition(full_conversation)

    st.subheader("🧠 Final Assessment")

    if classification == "risky":
        speak_text("This may be risky. Please consult a healthcare professional.")
        st.error("⚠️ Risky condition detected.\n\n" + explanation)
    elif classification == "normal":
        speak_text("This appears to be normal.")
        st.success("✅ The condition seems normal.\n\n" + explanation)
    else:
        speak_text("I'm not sure. Please try again or consult a doctor.")
        st.warning("⚠️ Unable to classify the condition.\n\n" + explanation)
