from dotenv import load_dotenv
import streamlit as st
import os
from PIL import Image
import google.generativeai as genai

# Load environment variables from .env file
load_dotenv()

# Configure the Generative AI model with the API key from environment variables
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Load the Gemini pro vision model
model = genai.GenerativeModel('gemini-pro-vision')

def get_gemini_response(input_prompt, image, user_input):
    response = model.generate_content([input_prompt, image[0], user_input])
    return response.text

def input_image_details(uploaded_file):
    if uploaded_file is not None:
        # Read the file into bytes
        bytes_data = uploaded_file.getvalue()
        image_parts = [
            {
                "mime_type": uploaded_file.type,  # Get the mime type of the uploaded file
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")

# Initialize Streamlit app
st.set_page_config(page_title="MultiLanguage Invoice Reader", layout='wide')

st.title("🧾 MultiLanguage Invoice Reader")
st.write("""
Welcome to the MultiLanguage Invoice Reader
         ! This application leverages advanced Generative AI to analyze invoices in multiple languages.
Simply upload an image of an invoice and provide a prompt to get detailed information.
""")

st.sidebar.header("Upload and Input")
user_input = st.sidebar.text_input("Input Prompt: ", key="input", help="Enter your query about the invoice")
uploaded_file = st.sidebar.file_uploader("Choose an image of the invoice...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    st.sidebar.image(uploaded_file, caption="Uploaded Image.", use_column_width=True)

submit = st.sidebar.button("Analyze Invoice")

input_prompt = """
You are an expert in understanding invoices. We will upload an image as an invoice
and you will have to answer any questions based on the uploaded invoice image.
"""

# Main section to display results
if submit:
    with st.spinner("Processing the invoice..."):
        try:
            image_data = input_image_details(uploaded_file)
            response = get_gemini_response(input_prompt, image_data, user_input)
            st.subheader("The Response is:")
            st.write(response)
        except FileNotFoundError as e:
            st.error(f"Error: {str(e)}")
        except Exception as e:
            st.error(f"An unexpected error occurred: {str(e)}")
else:
    st.info("Please upload an image and provide a prompt to analyze the invoice.")
