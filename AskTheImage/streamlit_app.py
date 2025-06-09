import streamlit as st
import google.generativeai as genai
from PIL import Image
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure Gemini API
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
genai.configure(api_key=GEMINI_API_KEY)

def extract_text_from_image(image_file):
    """Extract text from an image using Gemini Vision API."""
    try:
        # Open the image using PIL
        image = Image.open(image_file)
        
        # Initialize Gemini model
        model = genai.GenerativeModel('gemini-1.5-flash-latest')
        
        # Extract text using Gemini
        response = model.generate_content(["Extract all text from this image. Return only the extracted text, nothing else.", image])
        
        extracted_text = response.text.strip()
        
        if not extracted_text:
            return "No text could be extracted from the image."
        
        return extracted_text
    except Exception as e:
        return f"Error processing image: {str(e)}"

def get_gemini_response(extracted_text, user_query):
    """Get response from Gemini API based on extracted text and user query."""
    try:
        # Initialize Gemini model
        model = genai.GenerativeModel('gemini-1.5-flash-latest')
        
        # Construct prompt
        prompt = f"""Context from image: {extracted_text}

User query: {user_query}

Please provide a helpful response based on the above context and query."""
        
        # Generate response
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error getting response from Gemini: {str(e)}"

def main():
    st.title("Ask The Image")
    st.write("Upload an image and ask questions about its content!")
    
    # File uploader
    uploaded_file = st.file_uploader("Choose an image file", type=['png', 'jpg', 'jpeg'])
    
    # Text input for user query
    user_query = st.text_input("What would you like to know about the image?")
    
    if uploaded_file is not None and user_query:
        # Display the uploaded image
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image", use_column_width=True)
        
        # Process button
        if st.button("Process"):
            with st.spinner("Processing..."):
                # Extract text from image
                extracted_text = extract_text_from_image(uploaded_file)
                
                # Display extracted text
                st.subheader("Extracted Text:")
                st.write(extracted_text)
                
                # Get and display Gemini response
                st.subheader("AI Response:")
                response = get_gemini_response(extracted_text, user_query)
                st.write(response)

if __name__ == "__main__":
    main() 