import streamlit as st
import google.generativeai as genai
import os 
from dotenv import load_dotenv
load_dotenv() # loading all the environment variables
from PIL import Image


genai.configure(api_key=os.getenv("GOOGLLE_API_KEY"))

def get_gemini_response(input_prompt,image):
    model = genai.GenerativeModel('gemini-pro-vision')
    response = model.generate_content([input_prompt,image[0]])
    return response.text

def input_image_setup(upload_file):
    # Check if a file has been uploaded 
    if upload_file is not None:
        bytes_data = upload_file.getvalue()

        image_parts = [
            {
                'mime_type':upload_file.type,
                'data':bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError('No File Uploaded')
    
## Iniitalize Streamlit app
    
st.set_page_config(page_title = "Calories Advisor APP")

st.header("Calories Advisor APP")

upload_file = st.file_uploader('Choose an Image...',type=["jpg","jpeg","png"])

image = ""

if upload_file is not None:
    image = Image.open(upload_file)
    st.image(image,caption="Uploaded Image.",use_column_width=True)

submit = st.button('Tell me about the total calories')

input_prompt="""
You are an expert in nutritionist where you need to see the food items from the image
               and calculate the total calories, also provide the details of every food items with calories intake
               is below format

               1. Item 1 - no of calories
               2. Item 2 - no of calories
               ----
               ----
        
        Finally you can also mention whether the food is healthy or not and also mention the percentage splot ratio of carbohydrates, fats, fibers, suger and other important things required in our diet


"""

if submit:
    image_data = input_image_setup(upload_file)

    response = get_gemini_response(input_prompt,image_data)

    st.header('The Response Is')
    
    st.write(response)