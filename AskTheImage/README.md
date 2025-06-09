# Ask The Image

A cost-effective multimodal LLM application that processes images to extract text and uses Google's Gemini API to generate intelligent responses based on the extracted content and user queries.

## Features

- Image-to-Text conversion using Google Gemini Vision API
- Natural language query processing
- Integration with Google Gemini 1.5 Flash API
- User-friendly Streamlit interface
- Cost-effective implementation using Gemini's multimodal capabilities

## Prerequisites

- Python 3.9 or higher
- Google Gemini API key

## Installation

1. Clone this repository:
```bash
git clone https://github.com/yourusername/AskTheImage.git
cd AskTheImage
```

2. Install Python dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
- Copy `.env.example` to `.env`
- Add your Google Gemini API key to the `.env` file

## Usage

1. Start the Streamlit app:
```bash
streamlit run streamlit_app.py
```

2. Open your web browser and navigate to the provided local URL (typically http://localhost:8501)

3. Upload an image containing text

4. Enter your question about the image content

5. Click "Process" to get the AI-generated response

## Cost Optimization

This project is designed to be cost-effective by:
- Using Gemini's multimodal capabilities for both text extraction and response generation
- Implementing the Gemini 1.5 Flash model for efficient API usage
- Optimizing prompt construction to minimize token consumption
- Deploying on free-tier platforms (Streamlit Community Cloud)

## Future Enhancements

- Support for multiple image formats
- Batch processing capabilities
- Enhanced error handling and retry mechanisms
- Integration with additional LLM providers
- Support for audio-to-text conversion

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details. 