import streamlit as st
import os
import base64
import asyncio
from main import VoiceAssistant
import requests
import io
import wave

def load_css():
    st.markdown("""
    <style>
    .avatar {
        width: 150px;
        height: 150px;
        border-radius: 50%;
        margin: 0 auto;
        display: flex;
        align-items: center;
        justify-content: center;
        background-color: #4CAF50;
        color: white;
        font-size: 60px;
        border: 3px solid #2E7D32;
        box-shadow: 0 4px 8px 0 rgba(0,0,0,0.2);
    }
    .pulse {
        animation: pulse 2s infinite;
    }
    @keyframes pulse {
        0% { box-shadow: 0 0 0 0 rgba(76, 175, 80, 0.7); }
        70% { box-shadow: 0 0 0 15px rgba(76, 175, 80, 0); }
        100% { box-shadow: 0 0 0 0 rgba(76, 175, 80, 0); }
    }
    .language-btn {
        margin: 5px;
        padding: 10px 15px;
        border-radius: 20px;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

def main():
    load_css()
    
    st.title("🤖 Voice Assistant")
    
    if 'assistant' not in st.session_state:
        st.session_state.assistant = VoiceAssistant()
        st.session_state.recording = False
        st.session_state.selected_lang = None
        st.session_state.avatar_pulse = False
        st.session_state.audio_bytes = None
    
    st.markdown("""
    <div class="avatar %s">
        🤖
    </div>
    """ % ("pulse" if st.session_state.avatar_pulse else ""), unsafe_allow_html=True)
    
    st.subheader("Select Your Language")
    lang_cols = st.columns(5)
    languages = {
        "English": "en-IN",
        "Hindi": "hi-IN",
        "Tamil": "ta-IN",
        "Telugu": "te-IN",
        "Kannada": "kn-IN"
    }
    
    for i, (lang_name, lang_code) in enumerate(languages.items()):
        with lang_cols[i]:
            if st.button(lang_name, key=f"lang_{lang_code}", use_container_width=True):
                st.session_state.selected_lang = lang_code
                st.session_state.assistant.stt_engine.selected_language = lang_code
                st.success(f"Selected: {lang_name}")
    
    if st.session_state.selected_lang:
        if st.button("🎤 Start Recording (10 seconds)", 
                    disabled=st.session_state.recording,
                    type="primary"):
            
            st.session_state.recording = True
            st.session_state.avatar_pulse = True
            st.session_state.audio_bytes = None
            
            with st.spinner(f"Recording in {list(languages.keys())[list(languages.values()).index(st.session_state.selected_lang)]}..."):
                transcription, source_lang = st.session_state.assistant.stt_engine.speech_to_text()
                st.session_state.recording = False
                
                if not transcription:
                    st.error("No speech detected. Please try again.")
                    st.session_state.avatar_pulse = False
                    st.rerun()
                
                with st.status("Processing your request...", expanded=True) as status:
                    st.write(f"**You said:** {transcription}")
                    
                    english_text = st.session_state.assistant.translator.translate(transcription, source_lang)
                    st.write(f"**English translation:** {english_text}")
                    
                    agent_response = asyncio.run(st.session_state.assistant.agent_manager.get_agent_response(english_text))
                    st.write(f"**Assistant response:** {agent_response}")
                    
                    native_text = st.session_state.assistant.native_translator.translate(agent_response, source_lang)
                    st.write(f"**Native response:** {native_text}")
                    
                    st.write("Generating speech...")
                    try:
                        payload = {
                            "inputs": [native_text],
                            "target_language_code": source_lang,
                            **st.session_state.assistant.tts_engine.default_params
                        }
                        
                        response = requests.post(
                            st.session_state.assistant.tts_engine.api_url,
                            json=payload,
                            headers=st.session_state.assistant.tts_engine.headers
                        )
                        
                        if response.status_code == 200:
                            audio_data = base64.b64decode(response.json()["audios"][0])
                            with io.BytesIO() as wav_buffer:
                                with wave.open(wav_buffer, "wb") as wav_file:
                                    wav_file.setnchannels(1)
                                    wav_file.setsampwidth(2)
                                    wav_file.setframerate(22050)
                                    wav_file.writeframes(audio_data)
                                st.session_state.audio_bytes = wav_buffer.getvalue()
                            
                            status.update(label="Processing complete!", state="complete")
                        else:
                            raise Exception(f"API Error: {response.status_code}")
                    except Exception as e:
                        st.error(f"Error generating speech: {str(e)}")
                        st.session_state.avatar_pulse = False
                        status.update(label="Processing failed", state="error")
                        st.rerun()
            
            if st.session_state.audio_bytes:
                st.audio(st.session_state.audio_bytes, format="audio/wav")
                audio_html = f"""
                    <audio autoplay>
                        <source src="data:audio/wav;base64,{base64.b64encode(st.session_state.audio_bytes).decode()}" type="audio/wav">
                    </audio>
                    <script>
                        document.querySelector('audio').play().catch(e => console.log('Autoplay prevented:', e));
                    </script>
                """
                st.components.v1.html(audio_html, height=0)
    else:
        st.warning("Please select a language first")

if __name__ == "__main__":
    main()