import streamlit as st
import google.generativeai as genai
import re

# Configure Gemini
genai.configure(api_key="AIzaSyC9jEg8Icw6kMPs0tdncQKUCGtdeI_xINo")  # Replace with your actual API key
model = genai.GenerativeModel('gemini-2.0-flash')

# Page Config
st.set_page_config(page_title="Parenting Product Advisor", layout="wide")

# CSS Styling
st.markdown("""
<style>
    .product-card {
        border-radius: 10px;
        padding: 15px;
        margin: 10px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        transition: transform 0.2s;
        background: white;
    }
    .product-card:hover {
        transform: scale(1.02);
        box-shadow: 0 6px 12px rgba(0,0,0,0.15);
    }
    .product-image {
        width: 100%;
        height: 200px;
        object-fit: contain;
        border-radius: 8px;
        margin-bottom: 10px;
    }
    .product-title {
        font-weight: bold;
        margin: 5px 0;
        height: 60px;
        overflow: hidden;
    }
    .product-price {
        color: #B12704;
        font-size: 18px;
        font-weight: bold;
        margin: 5px 0;
    }
    .product-link {
        display: block;
        background: #FFD814;
        color: #0F1111;
        text-align: center;
        padding: 8px;
        border-radius: 5px;
        text-decoration: none;
        font-weight: bold;
        margin-top: 10px;
    }
    .product-link:hover {
        background: #F7CA00;
    }
</style>
""", unsafe_allow_html=True)

# Product database (sample data - in real app, you'd use API calls)
SAMPLE_PRODUCTS = {
    "baby": [
        {
            "name": "Philips Avent Natural Baby Bottle",
            "image": "https://m.media-amazon.com/images/I/71QY1X5ZkIL._SL1500_.jpg",
            "price": "₹1,299",
            "link": "https://www.amazon.in/Philips-Avent-Natural-Baby-Bottle/dp/B00J5K4Z1Q"
        },
        {
            "name": "Mee Mee Baby Pacifier",
            "image": "https://m.media-amazon.com/images/I/61sxZ5mJNBL._SL1500_.jpg",
            "price": "₹199",
            "link": "https://www.amazon.in/Mee-Baby-Orthodontic-Pacifier-6-18/dp/B00K6JQ9N4"
        }
    ],
    "mom": [
        {
            "name": "Mothercare Pregnancy Pillow",
            "image": "https://m.media-amazon.com/images/I/71JZG5J5ZJL._SL1500_.jpg",
            "price": "₹2,999",
            "link": "https://www.amazon.in/Mothercare-Pregnancy-Pillow-C-Shaped-White/dp/B07D5V5X5F"
        },
        {
            "name": "Pigeon Nursing Bra",
            "image": "https://m.media-amazon.com/images/I/61Q8S7n3VVL._SL1500_.jpg",
            "price": "₹499",
            "link": "https://www.amazon.in/Pigeon-Womens-Maternity-Nursing-38B/dp/B07D5V5X5F"
        }
    ]
}

def get_recommendations(user_type, answers):
    """Get AI recommendations and map to real product data"""
    if user_type == "baby":
        prompt = f"""Recommend exactly 5 baby products for:
        - Age: {answers['age']}
        - Need: {answers['need']}
        - Preference: {answers['preference']}
        - Challenge: {answers['challenge']}
        
        Return ONLY product names in this exact numbered format:
        1. Product Name One
        2. Product Name Two
        3. Product Name Three
        4. Product Name Four
        5. Product Name Five"""
    else:
        prompt = f"""Recommend exactly 5 maternity products for:
        - Trimester: {answers['trimester']}
        - Concern: {answers['concern']}
        - Need: {answers['need']}
        - Budget: {answers['budget']}
        
        Return ONLY product names in this exact numbered format:
        1. Product Name One
        2. Product Name Two
        3. Product Name Three
        4. Product Name Four
        5. Product Name Five"""
    
    response = model.generate_content(prompt)
    
    # More robust parsing of the response
    product_names = []
    for line in response.text.split("\n"):
        line = line.strip()
        if not line:
            continue
            
        # Handle different possible response formats
        if ". " in line:
            try:
                product_name = line.split(". ", 1)[1]  # Split on first ". " only
                product_names.append(product_name)
            except IndexError:
                continue
        elif line[0].isdigit() and " " in line:  # Format like "1 Product Name"
            try:
                product_name = line.split(" ", 1)[1]
                product_names.append(product_name)
            except IndexError:
                continue
        elif line.startswith("- "):  # Bullet point format
            product_names.append(line[2:])
    
    # Fallback if we couldn't parse enough products
    if len(product_names) < 5:
        st.warning(f"Could only find {len(product_names)} products. Using sample products to complete recommendations.")
        product_names += ["Baby Bottle", "Pacifier", "Diapers", "Baby Wipes", "Baby Clothes"][len(product_names):5]
        product_names = product_names[:5]
    
    # In real app, you would query your product database/API here
    # For demo, we'll use sample products that match the names
    recommended_products = []
    for name in product_names:
        found = False
        for product in SAMPLE_PRODUCTS[user_type]:
            if name.lower() in product["name"].lower():
                recommended_products.append(product)
                found = True
                break
        
        if not found:
            # Fallback if product not found
            recommended_products.append({
                "name": name,
                "image": "https://via.placeholder.com/300x300?text=Product+Image",
                "price": "₹---",
                "link": "#"
            })
    
    return recommended_products[:5]  # Return max 5 products

# Main App
st.title("👶🤰 Parenting Product Finder")

user_type = st.radio("Who are you shopping for?", ["Baby", "Mom"], horizontal=True).lower()

if user_type == "baby":
    with st.form("baby_form"):
        age = st.selectbox("Baby's Age", ["Newborn (0-3 months)", "Infant (3-12 months)", "Toddler (1-3 years)"])
        need = st.selectbox("Primary Need", ["Feeding", "Sleeping", "Diapering", "Playtime", "Health & Safety"])
        preference = st.selectbox("Preferences", ["Organic", "Budget-friendly", "Premium", "Eco-friendly"])
        challenge = st.selectbox("Current Challenge", ["Colic/Gas", "Sleep regression", "Teething", "Diaper rash", "None"])
        
        if st.form_submit_button("Find Products"):
            recommendations = get_recommendations("baby", {
                "age": age,
                "need": need,
                "preference": preference,
                "challenge": challenge
            })
            
            st.session_state.recommendations = recommendations
else:
    with st.form("mom_form"):
        trimester = st.selectbox("Pregnancy Stage", ["First trimester", "Second trimester", "Third trimester", "Postpartum"])
        concern = st.selectbox("Main Concern", ["Comfort", "Nutrition", "Maternity wear", "Baby preparation", "Postpartum care"])
        need = st.selectbox("Specific Need", ["Back pain relief", "Better sleep", "Skin care", "Nursing preparation"])
        budget = st.selectbox("Budget", ["Economy (Under ₹500)", "Mid-range (₹500-₹2000)", "Premium (₹2000+)"])
        
        if st.form_submit_button("Find Products"):
            recommendations = get_recommendations("mom", {
                "trimester": trimester,
                "concern": concern,
                "need": need,
                "budget": budget
            })
            
            st.session_state.recommendations = recommendations

# Display recommendations if available
if "recommendations" in st.session_state:
    st.header("Recommended Products")
    cols = st.columns(3)
    
    for i, product in enumerate(st.session_state.recommendations):
        with cols[i % 3]:
            st.markdown(f"""
            <div class="product-card">
                <img src="{product['image']}" class="product-image">
                <div class="product-title">{product['name']}</div>
                <div class="product-price">{product['price']}</div>
                <a href="{product['link']}" target="_blank" class="product-link">View on Amazon</a>
            </div>
            """, unsafe_allow_html=True)

    if st.button("Search Again"):
        del st.session_state.recommendations
        st.rerun()