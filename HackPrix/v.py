import streamlit as st

import pyttsx3

import speech_recognition as sr

import google.generativeai as genai



# Configure Gemini API

genai.configure(api_key="AIzaSyC9jEg8Icw6kMPs0tdncQKUCGtdeI_xINo")  # Replace with your key



# Text-to-Speech

def speak_text(text):

    engine = pyttsx3.init()

    engine.say(text)

    engine.runAndWait()



# Speech-to-Text

def speech_to_text():

    recognizer = sr.Recognizer()

    with sr.Microphone() as source:

        recognizer.adjust_for_ambient_noise(source)

        audio = recognizer.listen(source)

    try:

        return recognizer.recognize_google(audio)

    except sr.UnknownValueError:

        speak_text("Sorry, I didn't catch that.")

        return ""

    except sr.RequestError:

        speak_text("Speech recognition service issue.")

        return ""



# Gemini: Generate follow-up question

def generate_follow_up(symptom_description):

    model = genai.GenerativeModel("gemini-2.0-flash")

    prompt = f"""

You are helping a pregnant woman understand her symptoms better. Based on this description:



"{symptom_description}"



Ask one short, kind follow-up question to learn more. Keep it gentle and simple.

"""

    response = model.generate_content(prompt)

    return response.text.strip()



# Gemini: Final Classification

def classify_condition(full_input):

    model = genai.GenerativeModel("gemini-1.5-flash")

    prompt = f"""

A pregnant woman reported the following symptoms and answers:



"{full_input}"



Classify this entire input as either "normal" or "risky". 

Only respond with one word: "normal" or "risky".

"""

    response = model.generate_content(prompt)

    result = response.text.strip().lower()

    return result if result in ["normal", "risky"] else "unknown"



# Streamlit UI

st.title("🤰 Pregnancy Symptom Checker")



if st.button("🎤 Start Check"):

    conversation_parts = []



    # Step 1: Initial problem

    speak_text("Please describe the problem you are experiencing.")

    initial_input = speech_to_text()

    st.write(f"*You said:* {initial_input}")

    conversation_parts.append(f"Initial: {initial_input}")



    # Step 2: Follow-up question based on input

    follow_up_1 = generate_follow_up(initial_input)

    speak_text(follow_up_1)

    st.write(f"*Follow-up 1:* {follow_up_1}")

    answer1 = speech_to_text()

    st.write(f"*Answer:* {answer1}")

    conversation_parts.append(f"{follow_up_1} {answer1}")



    # Step 3: General Question 1

    q2 = "Have you felt any unusual movements or cramps recently?"

    speak_text(q2)

    st.write(f"*Follow-up 2:* {q2}")

    answer2 = speech_to_text()

    st.write(f"*Answer:* {answer2}")

    conversation_parts.append(f"{q2} {answer2}")



    # Step 4: General Question 2

    q3 = "Are you getting enough sleep and rest?"

    speak_text(q3)

    st.write(f"*Follow-up 3:* {q3}")

    answer3 = speech_to_text()

    st.write(f"*Answer:* {answer3}")

    conversation_parts.append(f"{q3} {answer3}")



    # Step 5: Combine and classify

    full_conversation = " ".join(conversation_parts)

    classification = classify_condition(full_conversation)



    st.subheader("🧠 Final Classification")

    if classification == "risky":

        speak_text("This may be risky. Please consult a healthcare professional.")

        st.error("⚠ This may be risky. Consult a healthcare professional.")

    elif classification == "normal":

        speak_text("This appears to be normal.")

        st.success("✅ The condition seems normal.")

    else:

        speak_text("I couldn't determine the condition. Please try again.")

        st.warning("⚠ Unable to classify the condition.")