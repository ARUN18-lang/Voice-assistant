import asyncio
from dotenv import load_dotenv
from stt import SarvamSpeechToText
from translate import SarvamTranslator
from translate1 import SarvamNativeTranslator
from tts import SarvamTextToSpeech
from agent import Agent

class VoiceAssistant:
    def __init__(self):
        load_dotenv()
        
        self.stt_engine = SarvamSpeechToText()
        self.translator = SarvamTranslator()
        self.agent_manager = Agent()
        self.tts_engine = SarvamTextToSpeech()
        self.native_translator = SarvamNativeTranslator()

    async def run(self):
        try:
            while True:
                print("\nSpeak now...")
                transcription, source_lang = self.stt_engine.speech_to_text()
                
                if not transcription:
                    print("No speech detected. Try again.")
                    continue
                
                print(f"\nYou said ({source_lang}): {transcription}")
                
                english_text = self.translator.translate(transcription, source_lang)
                print(f"\nEnglish: {english_text}")
                
                print("\nThinking...")
                agent_response = await self.agent_manager.get_agent_response(english_text)
                print(f"\nAgent: {agent_response}")
                
                native_text = self.native_translator.translate(agent_response, source_lang)
                print(f"\nNative ({source_lang}): {native_text}")

                print("\nConverting response to speech...")
                self.tts_engine.convert_to_speech(
                    text=native_text,
                    target_language_code=source_lang,
                    output_prefix="response"
                )
                
        except KeyboardInterrupt:
            print("\nShutting down...")
        finally:
            await self.agent_manager.cleanup()

if __name__ == "__main__":
    assistant = VoiceAssistant()
    asyncio.run(assistant.run())