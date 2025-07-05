import streamlit as st
from PIL import Image
import io

from ocr_processor import OCRProcessor
from llm_client import LLMClient
from utils import extract_json_array, extract_json_object

ocr = OCRProcessor()
llm = LLMClient()

st.set_page_config(page_title="Menu Analyzer", layout="wide")
st.title("Menu Analyzer (OCR + LLM)")

uploaded_file = st.file_uploader("Upload a restaurant menu image", type=["jpg", "jpeg", "png"])

# Initialize session state
if "dishes" not in st.session_state:
    st.session_state.dishes = None
if "ocr_text" not in st.session_state:
    st.session_state.ocr_text = None

if uploaded_file:
    image = Image.open(io.BytesIO(uploaded_file.read()))
    st.image(image, caption="Uploaded Menu", use_container_width=True)

    if st.button("Extract Menu Items"):
        with st.spinner("Running OCR..."):
            st.session_state.ocr_text = ocr.extract_text(image)

        with st.spinner("Identifying dishes..."):
            prompt = f"""
Extract only the dish names from the following restaurant menu text.

- Ignore prices, numbers, and currency symbols like ₹, Rs, INR, etc.
- Exclude any descriptions or section headers like "Main Course", "Soups", etc.
- Return only dish names as a valid JSON array of strings.
- No explanation, no markdown. Only a JSON array.

Menu:
{st.session_state.ocr_text}
"""
            dish_list_text = llm.query(prompt)

            if dish_list_text:
                try:
                    dishes = extract_json_array(dish_list_text)
                    st.session_state.dishes = dishes if dishes else None
                except Exception as e:
                    st.error(f"Dish List JSON Decode Error: {e}")
                    st.text(dish_list_text)

# Show dish selector
if st.session_state.dishes:
    st.markdown("### Extracted Dishes")
    selected_dish = st.selectbox("Select a dish", st.session_state.dishes)

    if selected_dish:
        with st.spinner("Fetching dish details..."):
            detail_prompt = f"""
Provide details about the dish "{selected_dish}" in **valid JSON only**.

Required format:
{{
  "description": "...",
  "image_url": "https://...",
  "ingredients": ["item1", "item2", "..."],  # Ensure list is closed properly
  "nutrition": {{
    "calories": "... kcal",
    "protein": "... g",
    "fat": "... g",
    "carbs": "... g"
  }}
}}

Do not explain or add extra text. Only output JSON.
Ensure all brackets and quotes are closed properly.
"""

            detail_text = llm.query(detail_prompt)
            try:
                data = extract_json_object(detail_text)
                st.markdown("### Dish Details")

                img_url = data.get("image_url", "")
                if img_url.startswith("http"):
                    st.image(img_url, caption=selected_dish, use_container_width=True)
                else:
                    st.warning("No image found. Showing fallback.")
                    st.image("https://via.placeholder.com/600x400?text=No+Image+Available", use_container_width=True)

                st.markdown(f"**Description:** {data.get('description', '')}")
                st.markdown("**Ingredients:** " + ", ".join(data.get("ingredients", [])))
                nutrition = data.get("nutrition", {})
                st.metric("Calories", nutrition.get("calories", "N/A"))
                col1, col2, col3 = st.columns(3)
                col1.metric("Protein", nutrition.get("protein", "N/A"))
                col2.metric("Fat", nutrition.get("fat", "N/A"))
                col3.metric("Carbs", nutrition.get("carbs", "N/A"))
            except Exception as e:
                st.error(f"JSON Parse Error: {e}")
                st.text(detail_text)
