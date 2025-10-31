import os
import streamlit as st
import requests
from PIL import Image
import io
import os

BACKEND_URL = os.environ.get("BACKEND_URL", "http://localhost:8000")

# ---------------------------
# App Configuration
# ---------------------------
st.set_page_config(
    page_title="Smart Recycle Bot",
    page_icon="♻️",
    layout="centered"
)

st.title("♻️ Smart Recycle Bot")
st.info("Classify your waste! Choose input method below.", icon="🌱")

# ---------------------------
# Sidebar - Documentation
# ---------------------------
with st.sidebar:
    st.header("How to use")
    st.markdown("""
    1. Select input type: **Text description** or **Image upload**.  
    2. Provide the item name or upload a photo.  
    3. Click '**Classify**' to get the recommended recycling category.
    """)

# ---------------------------
# Input Method Selection
# ---------------------------
input_method = st.radio(
    "Choose input method:",
    ("Text Description", "Image Upload")
)

# ---------------------------
# Text Input Section
# ---------------------------
if input_method == "Text Description":
    st.subheader("Describe your item")
    st.info(
        "Please provide item name of the item you want to recycle. "
        "Please do not include any additional details or descriptions.",
        icon="💡"
    )
    user_text = st.text_input("Type here:")
    if st.button("Classify"):
        if user_text.strip() != "":
            try:
                response = requests.post(
                    f"{BACKEND_URL}/classify_text",
                    json={"text": user_text}
                )
                result = response.json()
                st.success(result.get("response", "No response from backend"))
            except Exception as e:
                st.error(f"Error contacting backend: {e}")
        else:
            st.warning("Please type something!")

# ---------------------------
# Image Upload Section
# ---------------------------
elif input_method == "Image Upload":
    st.subheader("Upload a photo")
    uploaded_file = st.file_uploader("Choose an image...", type=["png", "jpg", "jpeg"])
    if uploaded_file is not None:
        img = Image.open(uploaded_file)
        st.image(img, caption="Uploaded image", use_container_width=True)

        if st.button("Classify Image"):
            try:
                img_bytes = io.BytesIO()
                img.save(img_bytes, format=img.format)
                img_bytes = img_bytes.getvalue()
                
                response = requests.post(
                    f"{BACKEND_URL}/classify_image",
                    files={"file": ("image", img_bytes, "image/jpeg")}
                )
                result = response.json()
                st.success(f"**The detected item from the image is:** {result.get('detected_item', 'No response from backend')}")
                st.success(f"**Instructions for disposal:** {result.get('instruction', 'No response from backend')}")
            except Exception as e:
                st.error(f"Error contacting backend: {e}")
