import streamlit as st
import google.generativeai as genai
from googleapiclient.discovery import build

# ✅ Page Configuration
st.set_page_config(page_title="MomCare: Your Personalized Baby Care Guide", layout="centered")

# ✅ Optional: Load CSS
def load_local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Uncomment if you have a style.css file
# load_local_css("style.css")

# ✅ Gemini API Setup
genai.configure(api_key="AIzaSyC9jEg8Icw6kMPs0tdncQKUCGtdeI_xINo")  # Replace with your API key
model = genai.GenerativeModel("gemini-2.0-flash")
chat = model.start_chat(history=[])

def get_gemini_response(prompt):
    try:
        response = chat.send_message(prompt)
        return response.text
    except Exception as e:
        return f"❌ Gemini Error: {e}"

# ✅ YouTube API Setup
YOUTUBE_API_KEY = "AIzaSyABTuIqQQS8Ooc4JaZA4owqCaEE5xZsPkI"  # Replace with your actual YouTube API key

def search_youtube_videos(query, max_results=6):
    youtube = build("youtube", "v3", developerKey=YOUTUBE_API_KEY)
    request = youtube.search().list(
        q=query,
        part="snippet",
        type="video",
        maxResults=max_results,
        safeSearch="strict"
    )
    response = request.execute()

    videos = []
    for item in response["items"]:
        video = {
            "title": item["snippet"]["title"],
            "description": item["snippet"]["description"],
            "video_id": item["id"]["videoId"]
        }
        videos.append(video)
    return videos

# ✅ Difficulty Adjustment
def adjust_difficulty(current, ease_score):
    if ease_score >= 80:
        return min(current + 1, 5)
    elif ease_score < 50:
        return max(current - 1, 1)
    return current

# ✅ Difficulty-based Keywords
DIFFICULTY_KEYWORDS = {
    1: "basic baby care tips",
    2: "baby care videos",
    3: "baby care guides for new moms",
    4: "advanced baby health tips",
    5: "expert parenting strategies"
}

# ✅ UI
st.markdown('<h1 style="text-align:center;">👩‍🍼MomCare: Your Personalized Baby Care Guide</h1>', unsafe_allow_html=True)
st.markdown('<h4 style="text-align:center;">Personalized baby care support for your motherhood journey</h4>', unsafe_allow_html=True)
st.markdown("---")

# ✅ Sidebar Input
with st.sidebar:
    st.header("Tell Us About You")
    name = st.text_input("Your Name")
    baby_age = st.text_input("baby age(months)", placeholder="e.g., 3 months")
    concern = st.text_input("Your Current Concern", placeholder="e.g., feeding")
    learning_pref = st.radio("Preferred Content Style", ["Visual", "Step-by-step Guides", "Doctor Talks"])
    ease_score = st.slider("Ease with Current Knowledge (1 = overwhelmed, 100 = confident)", 1, 100, 60)
    current_level = st.slider("Current Confidence Level (1-5)", 1, 5, 2)
    generate = st.button("Get Recommendations")

# ✅ Main Logic
if generate:
    # Adjust level
    new_level = adjust_difficulty(current_level, ease_score)

    # Query generation
    query = f"{DIFFICULTY_KEYWORDS[new_level]} - {concern} - {baby_age} - {learning_pref.lower()} content"

    # Get Gemini Tips
    gemini_prompt = f"What are some helpful tips for a new mom dealing with {concern.lower()} for a baby aged {baby_age}? it should be of 200 words and at the last it should say here are some recommended videos"
    tips = get_gemini_response(gemini_prompt)

    # Get YouTube Videos
    videos = search_youtube_videos(query)

    # Show Results
    st.subheader(f"🎥 Video Recommendations for {name or 'You'}")
    st.markdown(f'<div class="info">🧠 Confidence Level Adjusted to: <b>{new_level}</b></div>', unsafe_allow_html=True)

    st.markdown("### 👩‍⚕️ Gemini's Advice for You")
    st.info(tips)

    # Display Videos in 3 Columns
    cols = st.columns(3)
    for i, vid in enumerate(videos):
        video_url = f"https://www.youtube.com/watch?v={vid['video_id']}"
        with cols[i % 3]:
            st.markdown(f"""
                <div style="border:1px solid #ddd; border-radius:12px; padding:15px; margin-bottom:15px; background-color:#f9fafb;">
                    <a href="{video_url}" target="_blank">
                        <img src="https://img.youtube.com/vi/{vid['video_id']}/0.jpg" style="width:100%; border-radius:10px;" />
                    </a>
                    <h4 style="margin-top:10px;">🎥 {vid['title']}</h4>
                    <p>📖 {vid['description'][:100]}...</p>
                    <a href="{video_url}" target="_blank">🔗 Watch on YouTube</a>
                </div>
            """, unsafe_allow_html=True)
