import os
import google.generativeai as genai
import streamlit as st
from dotenv import load_dotenv
from PIL import Image

# Load all env variables from .env
load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Function for loading Gemini Pro Vision
model = genai.GenerativeModel("gemini-pro-vision")

def get_gemini_response(input, image, prompt):
    response= model.generate_content([input, image[0], prompt])
    return response.text

def input_image_details(uploaded_file):
    if uploaded_file is not None:
        # Read files into bytes
        bytes_data = uploaded_file.getvalue()

        image_parts = [
            {
                # mime type of uploaded file    
                "mime_type": uploaded_file.type, 
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")


# Streamlit
st.set_page_config(page_title="Multi Language Invoice Extractor")
st.header("Multi Language Invoice Extractor")

input=st.text_input("Input Prompt:", key="input")

uploaded_file=st.file_uploader("Choose image for invoice", type=["jpg", "jpeg", "png"])
image=""
if uploaded_file is not None:
    image=Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_column_width=True)

submit=st.button("Search Document")

input_prompt = """You are good at Invoice Data Extraction, I will upload invoices as images and ask questions on it as input,
return accurate answers."""

# If submit button is clicked
if submit:
    image_data = input_image_details(uploaded_file)
    response = get_gemini_response(input_prompt, image_data, input)
    st.subheader("Response :")
    st.write(response)