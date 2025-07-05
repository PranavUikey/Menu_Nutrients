import streamlit as st
from PIL import Image
import pytesseract
import openai
import io
import json
import re
import os

# Set OpenRouter API credentials
openai.api_key = os.getenv("OPENROUTER_API_KEY")
openai.api_base = "https://openrouter.ai/api/v1"

# Optional: Linux-specific path to Tesseract
pytesseract.pytesseract.tesseract_cmd = "/usr/bin/tesseract"  # Adjust if needed

# Function to extract JSON array safely
def extract_json_array(text):
    try:
        text = text.replace("“", '"').replace("”", '"').strip()
        match = re.search(r"\[\s*\".*?\"\s*\]", text, re.DOTALL)
        if not match:
            raise ValueError("No valid JSON array found.")
        return json.loads(match.group(0))
    except Exception as e:
        raise ValueError(f"Could not parse JSON array: {e}")

# Call OpenRouter LLM
def call_llm(prompt):
    try:
        response = openai.ChatCompletion.create(
            model="mistralai/mixtral-8x7b-instruct",  # You can switch models
            messages=[{"role": "user", "content": prompt}],
            temperature=0.4,
            max_tokens=800,
        )
        return response['choices'][0]['message']['content'].strip()
    except Exception as e:
        st.error(f"API error: {e}")
        return None

# Streamlit UI
st.set_page_config(page_title="🍽️ Menu Analyzer", layout="wide")
st.title("🍽️ Menu Analyzer (OCR + LLM with OpenRouter)")

uploaded_file = st.file_uploader("📷 Upload a restaurant menu image", type=["jpg", "jpeg", "png"])

# Use session state
if "dishes" not in st.session_state:
    st.session_state.dishes = None
if "ocr_text" not in st.session_state:
    st.session_state.ocr_text = None

if uploaded_file:
    file_bytes = uploaded_file.read()
    image = Image.open(io.BytesIO(file_bytes))
    st.image(image, caption="Uploaded Menu", use_column_width=True)

    if st.button("🧠 Extract Menu Items"):
        with st.spinner("🔍 Running OCR..."):
            ocr_text = pytesseract.image_to_string(image, lang="eng+hin+mar")  # Multilingual support
            st.session_state.ocr_text = ocr_text

        with st.spinner("🤖 Identifying dishes..."):
            prompt = f"""
Extract and return only the dish names from this menu text. Support Indian and multilingual dishes.

Only return a valid JSON array like:
["Dish 1", "Dish 2", "Dish 3"]

Do NOT include any explanation or markdown.

Menu:
{st.session_state.ocr_text}
"""
            dish_list_text = call_llm(prompt)
            if dish_list_text:
                try:
                    dishes = extract_json_array(dish_list_text)
                    if not dishes:
                        st.warning("No dishes found.")
                        st.session_state.dishes = None
                    else:
                        st.session_state.dishes = dishes
                except Exception as e:
                    st.error(f"❌ Dish List JSON Decode Error: {e}")
                    st.text(dish_list_text)
                    st.session_state.dishes = None

# Show dropdown if dishes found
if st.session_state.dishes:
    st.markdown("### 📋 Extracted Dishes")
    # st.code(json.dumps(st.session_state.dishes, indent=2), language="json")
    selected_dish = st.selectbox("🍽️ Select a dish", st.session_state.dishes)

    if selected_dish:
        with st.spinner("📦 Fetching dish details..."):
            detail_prompt = f"""
Give the following details about the dish: "{selected_dish}".

Return a valid JSON object in this format:
{{
  "description": "Brief about the dish",
  "image_url": "A valid image URL of the dish from the internet",
  "ingredients": ["item1", "item2", "..."],
  "nutrition": {{
    "calories": "... kcal",
    "protein": "... g",
    "fat": "... g",
    "carbs": "... g"
  }}
}}

Only return valid JSON. No explanation or markdown.
"""
            detail_text = call_llm(detail_prompt)
            try:
                # Extract the first JSON object
                match = re.search(r"\{.*\}", detail_text, re.DOTALL)
                if not match:
                    raise ValueError("No JSON object found.")
                data = json.loads(match.group(0))

                st.markdown("### 🍛 Dish Details")

                # Dish Image (with fallback)
                img_url = data.get("image_url", "")
                if img_url and img_url.startswith("http"):
                    st.image(img_url, caption=selected_dish, use_column_width=True)
                else:
                    st.warning("⚠️ No image found. Showing fallback.")
                    st.image("https://via.placeholder.com/600x400?text=No+Image+Available", caption="No Image Available", use_column_width=True)

                # Description
                st.markdown(f"**📝 Description:** {data.get('description', '')}")

                # Ingredients
                st.markdown("**🧂 Ingredients:**")
                st.markdown(", ".join(data.get("ingredients", [])))

                # Nutrition Info
                st.markdown("**🍽️ Nutrition Info:**")
                nutrition = data.get("nutrition", {})
                st.metric("Calories", nutrition.get("calories", "N/A"))
                col1, col2, col3 = st.columns(3)
                col1.metric("Protein", nutrition.get("protein", "N/A"))
                col2.metric("Fat", nutrition.get("fat", "N/A"))
                col3.metric("Carbs", nutrition.get("carbs", "N/A"))

            except Exception as e:
                st.error(f"❌ JSON Parse Error: {e}")
                st.text(detail_text)
