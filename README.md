# Speech-to-Speech Voice Assistant

This project is a voice assistant that converts spoken input into a translated spoken response by leveraging multiple APIs for speech-to-text, translation, and text-to-speech capabilities.

## Features

- **Speech-to-Text:** Transcribes user speech into text using the [`SarvamSpeechToText`](c:\Users\arun5\Desktop\STS\speech-to-speech\stt.py) module.
- **Translation:** Translates input text to English and back into the native language using [`SarvamTranslator`](c:\Users\arun5\Desktop\STS\speech-to-speech\translate.py) and [`SarvamNativeTranslator`](c:\Users\arun5\Desktop\STS\speech-to-speech\translate1.py).
- **Voice Agent:** Generates responses using a language model implemented in [`Agent`](c:\Users\arun5\Desktop\STS\speech-to-speech\agent.py).
- **Text-to-Speech:** Converts text responses into spoken output with [`SarvamTextToSpeech`](c:\Users\arun5\Desktop\STS\speech-to-speech\tts.py).
- **Web Interface:** Provides a user-friendly interface built with Streamlit ([`app.py`](c:\Users\arun5\Desktop\STS\speech-to-speech\app.py)) and an HTML template ([`templates/index.html`](c:\Users\arun5\Desktop\STS\speech-to-speech\templates\index.html)).

## Setup

1. **Environment Variables:**  
   Create a `.env` file in the project root with the required API keys. Refer to [`utils.py`](c:\Users\arun5\Desktop\STS\speech-to-speech\utils.py) for details on the keys needed:
   - `SARVAM_API_KEY`
   - `SERPAPI_API_KEY`
   - `GROQ_API_KEY`
   - (Other keys as required)

2. **Install Dependencies:**  
   Install the required packages using:
   ```sh
   pip install -r requirements.txt

3. **Python Version:**
Ensure you are using Python 3.11 (as specified in .python-version).

**Running the Project**
    Command-Line Interface (CLI):
    To run the voice assistant from the terminal:

    python main.py

    Web Interface (Streamlit):
    To launch the web-based interface:

    streamlit run app.py



**Acknowledgements**

LangChain for language model integration.
Sarvam API for translation and text-to-speech services.
