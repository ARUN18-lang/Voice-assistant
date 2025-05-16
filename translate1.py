import re
import requests
import time
from utils import get_sarvam_api_key

class SarvamNativeTranslator:
    
    def __init__(self):
        self.api_url = "https://api.sarvam.ai/translate"
        self.api_key = get_sarvam_api_key()
        self.headers = {
            "api-subscription-key": self.api_key,
            "Content-Type": "application/json"
        }
        
        # Default params will be set during translation
        self.default_template = {
            "speaker_gender": "Male",
            "mode": "classic-colloquial",
            "model": "mayura:v1",
            "enable_preprocessing": True
        }

    @staticmethod
    def _split_into_sentences(text):
        return re.split(r'(?<=[.!?])\s+', text.strip())

    def _translate_sentence(self, sentence, target_lang):
        payload = {
            "source_language_code": "en-IN",  
            "target_language_code": target_lang,
            "input": sentence,
            **self.default_template
        }

        try:
            response = requests.post(self.api_url, json=payload, headers=self.headers)
            if response.status_code == 200:
                return response.json().get("translated_text", "")
            print(f"Translation API error: {response.status_code}")
            return None
        except Exception as e:
            print(f"Translation request failed: {e}")
            return None

    def translate(self, text, target_language_code):
        """
        Translate English text to the target language
        Args:
            text: English text to translate
            target_language_code: Language code to translate to (e.g., 'hi-IN')
        """
        if not text or not target_language_code:
            return ""
            
        sentences = self._split_into_sentences(text)
        translated_text = []
        
        for sentence in sentences:
            if not sentence.strip():
                continue
                
            translation = self._translate_sentence(sentence, target_language_code)
            if translation:
                translated_text.append(str(translation))
            time.sleep(0.3) 
        
        return ' '.join(translated_text)