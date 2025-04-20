import streamlit as st
import requests
import base64
from io import BytesIO
from PIL import Image

# Access Hugging Face API Token from Streamlit Secrets
API_TOKEN = st.secrets["API_TOKEN"]

# Hugging Face model endpoint for image generation (use the correct model ID)
endpoint = "https://api-inference.huggingface.co/models/CompVis/stable-diffusion-v-1-4-original"

# Function to generate image from text input
def generate_image(prompt):
    headers = {"Authorization": f"Bearer {API_TOKEN}"}
    payload = {
        "inputs": prompt,
    }
    
    # Request to Hugging Face API
    response = requests.post(endpoint, headers=headers, json=payload)
    
    if response.status_code == 200:
        try:
            # Extract base64-encoded image from response
            image_data = response.json()[0]['image']
            image = Image.open(BytesIO(base64.b64decode(image_data)))
            return image
        except Exception as e:
            st.error(f"Error decoding image: {e}")
            return None
    else:
        st.error(f"Error: {response.status_code} - {response.text}")
        return None

# Streamlit App UI
st.set_page_config(page_title="Text to Image Generator", layout="centered")
st.title("🎨 Text to Image Generator")
st.write("Enter a description to generate an image based on it!")

# Input area for prompt
prompt = st.text_area("Enter your text prompt:")

# Button to trigger image generation
if st.button("Generate Image"):
    if prompt:
        with st.spinner("Generating image..."):
            result = generate_image(prompt)
            if result:
                # Display generated image
                st.image(result, caption="Generated Image", use_column_width=True)
            else:
                st.error("Failed to generate image. Please try again.")
    else:
        st.warning("Please enter a text prompt.")
