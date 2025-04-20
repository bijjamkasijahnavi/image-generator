import streamlit as st
import requests

# Replace this with your real Hugging Face token
API_TOKEN = "hf_YOUR_REAL_TOKEN_HERE"

# Use Stable Diffusion v1.5 for clean educational diagrams
API_URL = "https://api-inference.huggingface.co/models/runwayml/stable-diffusion-v1-5"
HEADERS = {"Authorization": f"Bearer {API_TOKEN}"}

def generate_image(prompt):
    payload = {"inputs": prompt}
    response = requests.post(API_URL, headers=HEADERS, json=payload)

    if response.status_code == 200:
        return response.content  # Returns the raw image bytes
    else:
        st.error(f"❌ Failed to generate image (Status {response.status_code})")
        try:
            st.json(response.json())
        except:
            pass
        return None

st.set_page_config(page_title="📚 Student AI Image Generator", layout="centered")
st.title("📘 Study Image Generator")
st.write("Enter your study topic or description:")

user_input = st.text_input("✏️ Example: 'Labelled diagram of a plant cell'")

if st.button("Generate Image") and user_input:
    with st.spinner("🔄 Generating..."):
        image = generate_image(user_input)

    if image:
        st.image(image, caption=f"Prompt: {user_input}")
        st.success("✅ Image generated successfully!")
