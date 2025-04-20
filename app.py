import streamlit as st
import requests

# Access Hugging Face API Token from Streamlit Secrets
API_TOKEN = st.secrets["API_TOKEN"]

# Hugging Face model endpoint for image generation (use the correct model ID)
endpoint = "https://api-inference.huggingface.co/models/runwayml/stable-diffusion-v1-5"  # Replace with your model ID

# Function to generate image from text input
def generate_image(prompt):
    headers = {"Authorization": f"Bearer {API_TOKEN}"}
    payload = {
        "inputs": prompt,
    }
    
    # Request to Hugging Face API
    response = requests.post(endpoint, headers=headers, json=payload)
    
    if response.status_code == 200:
        return response.json()
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
                # Assuming result contains the image URL or base64-encoded image
                st.image(result[0]['image'], caption="Generated Image", use_column_width=True)
            else:
                st.error("Failed to generate image. Please try again.")
    else:
        st.warning("Please enter a text prompt.")
