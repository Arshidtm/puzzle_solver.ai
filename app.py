import google.generativeai as genai
import streamlit as st
import os
from PIL import Image  
import io 

# --- API Keys and Setup ---
google_api_key = os.environ.get("GOOGLE_API_KEY")

if not google_api_key:
    st.error("Please set the GOOGLE_API_KEY environment variable.")
    st.stop()

genai.configure(api_key=google_api_key)

# --- Gemini Model Configuration ---
generation_config = {
    "temperature": 1,
    'top_p': 0.95,
    'top_k': 40,
    'max_output_tokens': 8192,
    'response_mime_type': "text/plain",
}

model = genai.GenerativeModel(
    model_name="gemini-2.0-flash", 
    generation_config=generation_config
)

# --- Streamlit App ---
st.title("Image Text Extractor and Puzzle Solver")

uploaded_file = st.file_uploader("Upload an image of a puzzle", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:

    image_bytes = uploaded_file.read()

   
    try:
        image = Image.open(io.BytesIO(image_bytes)) 
        st.image(image, caption="Uploaded Image", use_column_width=True) 
    except Exception as e:
        st.error(f"Error opening image with PIL: {e}")
        st.stop()

    with st.spinner("Extracting text and attempting to solve the puzzle..."):
       
        try:
            response = model.generate_content([
                image, 
                "Extract all the text from the image.  Then, if the text appears to describe a math puzzle or logic puzzle, try to provide the solution.  If not a puzzle, just provide the extracted text.",
                "Image: extract text from image and solve puzzle",
            ])

            
            if response.text:
                st.subheader("Extracted Text and Potential Solution:")
                st.write(response.text)
            else:
                st.warning("No text could be extracted from the image.")

            if response.prompt_feedback: 
                st.write("Prompt Feedback:")
                st.write(response.prompt_feedback)


        except Exception as e:
            st.error(f"Error during Gemini API call: {e}")
else:
    st.info("Please upload an image to begin.")