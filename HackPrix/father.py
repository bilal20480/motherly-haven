import streamlit as st
import google.generativeai as genai

# 🔐 Set your API Key
genai.configure(api_key="AIzaSyC9jEg8Icw6kMPs0tdncQKUCGtdeI_xINo")  # Replace with your actual key

# Initialize Gemini model
model = genai.GenerativeModel("gemini-1.5-flash")

st.set_page_config(page_title="Husband Support Mode", layout="centered")
st.title("👨‍👩‍👦 Husband Support Mode")
st.markdown("#### Support your partner with care and understanding 💙")

# Select stage
phase = st.selectbox("What stage is your wife in?", ["Pregnancy", "Postpartum"])

# Substage dropdown
if phase == "Pregnancy":
    substage = st.selectbox("Select Trimester", ["First Trimester", "Second Trimester", "Third Trimester"])
else:
    substage = st.selectbox("Select Recovery Period", ["Week 1", "Week 2-4", "Month 2+", "C-section Recovery"])

# Husband's perspective
struggle = st.text_input("🧠 What is your partner struggling with?")
support_way = st.text_input("🤝 How do you want to help?")

# Generate empathetic tips
if st.button("Generate Support Tips"):
    with st.spinner("Thinking with you..."):

        prompt = f"""
Act as a supportive, emotionally intelligent guide for husbands whose wives are going through {phase.lower()} ({substage.lower()}).
The wife is currently struggling with: "{struggle}".
The husband wants to help her by: "{support_way}".

First, write 2–3 empathetic and encouraging sentences to the husband — acknowledge his care, reassure him he's doing his best, and validate how important his role is.

Then, give 5-7 short, actionable support tips in bullet points. Tips should be gentle, clear, and under 30 words each.

The tone must be kind, comforting, and respectful.

Finally, conclude with one sentence of motivation and hope for the husband.
"""

        try:
            response = model.generate_content(prompt)
            output = response.text
            st.success("💙 Here's something for you:")
            st.markdown(output)
        except Exception as e:
            st.error(f"Oops! Gemini had a moment:\n\n{e}")
