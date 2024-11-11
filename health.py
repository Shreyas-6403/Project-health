### Health Management APP
from dotenv import load_dotenv
load_dotenv()  # Load environment variables

import streamlit as st
import os
import google.generativeai as genai
from PIL import Image

# Configure API key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Function to load Google Gemini 1.5 Flash API and get response
def get_gemini_response(input_text, image, prompt):
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')  # Updated model
        response = model.generate_content([input_text, image[0], prompt])
        return response.text  # Access text attribute directly
    except Exception as e:
        st.error(f"Error calling API: {e}")
        return None

# Function to set up input image
def input_image_setup(uploaded_file):
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()
        image_parts = [
            {
                "mime_type": uploaded_file.type,
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")

# Initialize Streamlit app
st.set_page_config(page_title="Gemini Health App")
st.header("Gemini Health App")

# Get user input
user_input = st.text_input("Input Prompt: ", key="input")
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
image = ""

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image.", use_column_width=True)

submit = st.button("Tell me the total calories")

input_prompt = """
You are an expert nutritionist. You need to analyze the food items in the image and calculate the total calories. Also, provide details of each food item with calorie intake in the following format:

1. Item 1 - calories
2. Item 2 - calories
----
----
"""

# Handle button click
if submit and uploaded_file is not None and user_input:
    try:
        image_data = input_image_setup(uploaded_file)
        response_text = get_gemini_response(user_input, image_data, input_prompt)
        if response_text:
            st.subheader("The Response is")
            st.write(response_text)
    except Exception as e:
        st.error(f"An error occurred: {e}")
else:
    st.info("Please upload an image and enter an input prompt before submitting.")
