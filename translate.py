import re
import requests
import time
from utils import get_sarvam_api_key

class SarvamTranslator:
    
    def __init__(self):
        self.api_url = "https://api.sarvam.ai/translate"
        self.api_key = get_sarvam_api_key()
        self.headers = {
            "api-subscription-key": self.api_key,
            "Content-Type": "application/json"
        }
        
        self.default_params = {
            "target_language_code": "en-IN", 
            "speaker_gender": "Male",
            "mode": "classic-colloquial",
            "model": "mayura:v1",
            "enable_preprocessing": True
        }

    @staticmethod
    def _split_into_sentences(text):
        return re.split(r'(?<=[.!?])\s+', text.strip())

    def _translate_sentence(self, sentence, source_lang):
        payload = {
            "source_language_code": source_lang,
            "input": sentence,
            **self.default_params
        }

        try:
            response = requests.post(self.api_url, json=payload, headers=self.headers)
            if response.status_code == 200:
                return response.json().get("translated_text", "")
            return None
        except Exception:
            return None

    def translate(self, text, source_language_code):
        if not text or not source_language_code:
            return ""
            
        sentences = self._split_into_sentences(text)
        translated_text = []
        
        for sentence in sentences:
            if not sentence.strip():
                continue
                
            translation = self._translate_sentence(sentence, source_language_code)
            if translation:
                translated_text.append(str(translation))
            time.sleep(0.3)
        
        return ' '.join(translated_text)