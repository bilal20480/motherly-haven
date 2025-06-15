import streamlit as st
import google.generativeai as genai
import random

# Configure Gemini API
genai.configure(api_key="AIzaSyC9jEg8Icw6kMPs0tdncQKUCGtdeI_xINo")  # Replace with your key

def get_gemini_recommendations(prompt):
    model = genai.GenerativeModel("gemini-2.0-flash")
    response = model.generate_content(
        f"""
You are a product advisor for moms and babies.

Prompt: {prompt}

Based on the user's need, return a JSON list of exactly 6 useful products.
Each product must include:
- title
- short description
- mock price (e.g., ₹599)
- image URL (can be any valid placeholder)

Respond ONLY as a valid Python list of dictionaries like:
[
  {{
    "title": "Pregnancy Pillow",
    "description": "Supports belly and back during sleep.",
    "price": "₹1,499",
    "image": "https://via.placeholder.com/300"
  }},
  ...
]
        """
    )

    try:
        return eval(response.text)  # Gemini returns Python-style list
    except:
        return []

# UI
st.set_page_config(page_title="Mom & Baby Product Recommender", layout="centered")
st.title("🤰👶 Mom & Baby Product Recommender")

# Step 1: Choose category
st.subheader("Choose a category:")

col1, col2, col3 = st.columns(3)
selected_category = None

with col1:
    if st.button("Pregnant"):
        selected_category = "Pregnant"

with col2:
    if st.button("Postpartum"):
        selected_category = "Postpartum"

with col3:
    if st.button("Baby"):
        selected_category = "Baby"

# Step 2: Dropdown options based on category
prompt = ""
if selected_category == "Pregnant":
    options = [
        "I am in the first trimester",
        "I am in the third trimester",
        "I need help with sleep during pregnancy",
        "What do I need for hospital prep?",
        "How to reduce pregnancy back pain?"
    ]
    prompt = st.selectbox("Select a concern:", options)

elif selected_category == "Postpartum":
    options = [
        "I'm recovering after delivery",
        "I need nursing essentials",
        "How to reduce belly after delivery?",
        "Self-care tips after childbirth",
        "Help with breastfeeding support"
    ]
    prompt = st.selectbox("Select a concern:", options)

elif selected_category == "Baby":
    options = [
        "My baby is 3 months old",
        "My baby is teething",
        "Things needed for baby’s bath time",
        "Best toys for newborn",
        "Feeding items for infants"
    ]
    prompt = st.selectbox("Select a concern:", options)

# Step 3: Fetch recommendations
if prompt:
    st.markdown("### 🛍️ Recommended Products:")
    with st.spinner("Thinking..."):
        products = get_gemini_recommendations(prompt)

    if products:
        for product in products:
            st.image(product["image"], width=300)
            st.markdown(f"**{product['title']}**")
            st.markdown(product["description"])
            st.markdown(f"**Price:** {product['price']}")
            st.markdown("---")
    else:
        st.error("Could not fetch products. Try again.")
