import streamlit as st
import google.generativeai as genai

import streamlit as st
import google.generativeai as genai

def what_to_expect_feature():
    st.header("What to Expect Next Week")
    st.write("Discover what's coming up in your pregnancy journey")
    
    # User inputs
    current_week = st.slider("Current pregnancy week", 1, 39, 20, 
                           help="Select your current week to see what's coming next")
    next_week = current_week + 1
    
    col1, col2 = st.columns(2)
    with col1:
        mood = st.selectbox("How are you feeling today?", 
                          ["Happy", "Tired", "Anxious", "Calm", "Excited", "Overwhelmed"])
    with col2:
        activity = st.radio("Preferred activity", 
                          ["Yoga", "Walking", "Meditation", "Swimming", "Pilates", "None"])
    
    symptoms = st.multiselect("Current symptoms",
                            ["Back pain", "Nausea", "Swelling", "Mood swings", 
                             "Fatigue", "Food cravings", "Heartburn", "None"],
                            help="Select all that apply")
    
    high_risk = st.checkbox("High-risk pregnancy", help="Check if your doctor has classified your pregnancy as high-risk")
    
    if st.button(f"Show Week {next_week} Expectations"):
        # Enhanced prompt with medical tone and structure
        prompt = f"""Act as an experienced obstetrician. A patient is currently in week {current_week} and 
        asking about week {next_week} of pregnancy. Here's her profile:
        
        - Current mood: {mood}
        - Reported symptoms: {', '.join(symptoms) if symptoms else 'No significant symptoms'}
        - Preferred activity: {activity}
        - Pregnancy type: {'High-risk' if high_risk else 'Normal'}
        
        Provide a clinically accurate yet compassionate overview of week {next_week} with these sections:
        
        1. **Fetal Development Milestones**: 
        - Size comparison (fruit/vegetable)
        - Key organ developments
        - Movement patterns to expect
        
        2. **Maternal Changes**:
        - Physical changes (3-4 most common)
        - Emotional changes (mood-specific advice for {mood.lower()} patients)
        
        3. **Wellness Recommendation**:
        - Customized suggestion incorporating their preference for {activity.lower()}
        - Safety modifications if high-risk
        
        4. **Professional Advice**:
        - 3 specific action items (medical appointments, tests, preparations)
        - Red flags to watch for
        
        Close with an encouraging 2-sentence note emphasizing the uniqueness of her pregnancy journey.
        
        Use bullet points, avoid medical jargon, and maintain a warm but professional tone.
        """
        
        # Get Gemini response
        with st.spinner(f"Preparing your Week {next_week} guide..."):
            try:
                genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
                model = genai.GenerativeModel('gemini-2.0-flash')
                response = model.generate_content(prompt)
                
                # Display formatted response
                st.subheader(f"👶 Week {next_week} Pregnancy Guide")
                st.markdown("---")
                
                # Add week progression visual
                progress = next_week/40
                st.progress(progress, text=f"Pregnancy progress: {next_week}/40 weeks")
                
                st.markdown(response.text)
                
                # Add disclaimer
                st.markdown("---")
                st.caption("""
                ℹ️ This general information is not medical advice. Always consult your healthcare provider 
                about your specific pregnancy. Report any concerning symptoms immediately.
                """)
                
            except Exception as e:
                st.error("Couldn't generate recommendations. Please try again later.")
                if st.secrets.get("DEBUG"):
                    st.error(str(e))

# Example usage in your app:
what_to_expect_feature()