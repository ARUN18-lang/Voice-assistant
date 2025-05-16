import requests
import base64
import wave
from utils import get_sarvam_api_key

class SarvamTextToSpeech:
    
    def __init__(self):
        self.api_url = "https://api.sarvam.ai/text-to-speech"
        self.api_key = get_sarvam_api_key()
        self.headers = {
            "Content-Type": "application/json",
            "api-subscription-key": self.api_key
        }
        
        self.default_params = {
            "speaker": "meera",
            "model": "bulbul:v1",
            "pitch": 0,
            "pace": 1.0,
            "loudness": 1.0,
            "enable_preprocessing": True
        }
        
        self.audio_config = {
            "channels": 1,  
            "sample_width": 2,  
            "frame_rate": 22050  
        }

    def _split_text(self, text, chunk_size=500):
        return [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]

    def _save_audio_file(self, audio_data, filename):
        try:
            with wave.open(filename, "wb") as wav_file:
                wav_file.setnchannels(self.audio_config["channels"])
                wav_file.setsampwidth(self.audio_config["sample_width"])
                wav_file.setframerate(self.audio_config["frame_rate"])
                wav_file.writeframes(audio_data)
            return True
        except Exception as e:
            print(f"Error saving audio file: {e}")
            return False

    def convert_to_speech(self, text, target_language_code, output_prefix="output"):
        """
        Convert text to speech and save as WAV file(s).
        
        Args:
            text: The text to convert to speech
            target_language_code: Target language code (e.g., 'kn-IN')
            output_prefix: Prefix for output filenames
            
        Returns:
            list: Paths to generated audio files
        """
        if not text:
            raise ValueError("Text cannot be empty")
            
        if not target_language_code:
            raise ValueError("Target language code is required")

        chunks = self._split_text(text)
        audio_files = []
        print(f"target language code {target_language_code}")
        
        print(f"\nProcessing {len(chunks)} text chunk(s)...")

        for i, chunk in enumerate(chunks, 1):
            payload = {
                "inputs": [chunk],
                "target_language_code": target_language_code,
                **self.default_params
            }

            try:
                response = requests.post(
                    self.api_url,
                    json=payload,
                    headers=self.headers
                )

                if response.status_code == 200:
                    audio_data = base64.b64decode(response.json()["audios"][0])
                    filename = f"{output_prefix}_{i}.wav"
                    
                    if self._save_audio_file(audio_data, filename):
                        audio_files.append(filename)
                        print(f"Saved: {filename}")
                    else:
                        print(f"Failed to save chunk {i}")
                else:
                    print(f"Error for chunk {i}: {response.status_code}")
                    if response.text:
                        print(response.json())

            except Exception as e:
                print(f"Error processing chunk {i}: {e}")

        return audio_files


