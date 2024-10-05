import os
from PIL import Image
from dotenv import load_dotenv
import streamlit as st
import base64
import google.generativeai as genai

# Load environment variables from the .env file
load_dotenv()  # loading the environment variables
api_key = os.getenv("GOOGLE_API_KEY")
print(f" Loaded API Key: {api_key}")  # Debugging line to check if the API key is loaded correctly

# Configure the Generative AI with the API key
genai.configure(api_key=api_key)

# Load the Gemini Pro Vision model
model = genai.GenerativeModel('gemini-1.5-flash')

def get_response(input_text, image):
    if input_text != "":
        response = model.generate_content([input_text, image])
    else:
        response = model.generate_content(image)
    return response.text

# Initialize Streamlit app
st.set_page_config(page_title="Gemini Decode: Multilanguage Document Extraction by Gemini Pro")
st.header("Gemini Decode: Multilanguage Document Extraction by Gemini Pro")

# Function to set a background image (if needed)
def set_background(image_file):
    with open(image_file, "rb") as img:
        b64_image = base64.b64encode(img.read()).decode("utf-8")
    css = f"""
    <style>
    .stApp {{
        background: url(data:image/png;base64,{b64_image});
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
    }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

# Input text box for user input
input_prompt = st.text_input("Input:", key="input")

# File uploader for document images
uploaded_file = st.file_uploader("Choose an image of the document:", type=["jpg", "jpeg", "png"])
image = None

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_column_width=True)

# Button to submit the uploaded document
submit = st.button("Submit")

# Display introductory text
text = ("Utilizing Gemini Pro AI, this project effortlessly extracts vital information from diverse multilingual documents, "
        "transcending language barriers with precision and efficiency for enhanced productivity and decision-making.")
styled_text = f"<span style='font-family:serif;'>{text}</span>"
st.markdown(styled_text, unsafe_allow_html=True)

# Process the submitted document and get the response
if submit and image is not None:
    response = get_response(input_prompt, image)  # Pass input_prompt and image
    st.subheader("Bot Response:")
    st.write(response)
