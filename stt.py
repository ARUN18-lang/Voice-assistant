import pyaudio
import wave
import io
import os
import requests
from utils import get_sarvam_api_key

class SarvamSpeechToText:
    
    def __init__(self):
        self.api_url = "https://api.sarvam.ai/speech-to-text"
        self.api_key = get_sarvam_api_key()
        self.headers = {"api-subscription-key": self.api_key}
        
        self.language_options = {
            1: {"name": "English", "code": "en-IN"},
            2: {"name": "Hindi", "code": "hi-IN"},
            3: {"name": "Tamil", "code": "ta-IN"},
            4: {"name": "Telugu", "code": "te-IN"},
            5: {"name": "Kannada", "code": "kn-IN"}
        }
        
        self.FORMAT = pyaudio.paInt16
        self.CHANNELS = 1
        self.RATE = 16000
        self.CHUNK = 1024
        self.RECORD_SECONDS = 10
        
        self.audio_interface = pyaudio.PyAudio()
        self.selected_language = None

    def select_language(self):
        print("\nSelect Source Language:")
        for option, lang_info in self.language_options.items():
            print(f"{option} -> {lang_info['name']}")
        
        while True:
            try:
                lang_opt = int(input("Enter your choice (1-5): "))
                if lang_opt in self.language_options:
                    self.selected_language = self.language_options[lang_opt]['code']
                    return self.selected_language  
                else:
                    print("Invalid choice. Please enter a number between 1-5.")
            except ValueError:
                print("Invalid input. Please enter a number.")

    def _record_audio_chunk(self, stream, chunk_duration):
        frames = []
        for _ in range(0, int(self.RATE / self.CHUNK * chunk_duration)):
            data = stream.read(self.CHUNK)
            frames.append(data)
        return b"".join(frames)

    def _create_wav_buffer(self, audio_data):
        wav_buffer = io.BytesIO()
        with wave.open(wav_buffer, "wb") as wf:
            wf.setnchannels(self.CHANNELS)
            wf.setsampwidth(self.audio_interface.get_sample_size(self.FORMAT))
            wf.setframerate(self.RATE)
            wf.writeframes(audio_data)
        wav_buffer.seek(0)
        return wav_buffer

    def _transcribe_audio(self, audio_data):
        wav_buffer = self._create_wav_buffer(audio_data)
        
        request_data = {
            "language_code": self.selected_language,
            "model": "saarika:v2",
            "with_timestamps": False
        }
        
        files = {'file': ('audio.wav', wav_buffer, 'audio/wav')}
        
        try:
            response = requests.post(
                self.api_url,
                headers=self.headers,
                files=files,
                data=request_data
            )
            
            if response.status_code in (200, 201):
                return response.json().get("transcript", "")
            else:
                print(f"API request failed with status {response.status_code}")
                print("Response:", response.text)
                return None
                
        except Exception as e:
            print(f"Error during API request: {e}")
            return None
        finally:
            wav_buffer.close()

    def speech_to_text(self):
        if not self.selected_language:
            self.select_language()
        
        stream = self.audio_interface.open(
            format=self.FORMAT,
            channels=self.CHANNELS,
            rate=self.RATE,
            input=True,
            frames_per_buffer=self.CHUNK
        )
        
        print(f"\nRecording for {self.RECORD_SECONDS} seconds... Speak now!")
        
        audio_data = self._record_audio_chunk(stream, self.RECORD_SECONDS)
        
        stream.stop_stream()
        stream.close()
        
        transcription = self._transcribe_audio(audio_data)
        
        return transcription, self.selected_language  
    
    