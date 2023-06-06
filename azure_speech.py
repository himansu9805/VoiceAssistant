import os
import io
import azure.cognitiveservices.speech as speechsdk
from dotenv import load_dotenv

load_dotenv()

subscription_key = os.getenv('AZURE_SUBSCRIPTION_KEY')
region = os.getenv('AZURE_REGION')


def generate_tts_audio(text):
    speech_config = speechsdk.SpeechConfig(
        subscription=subscription_key, region=region)
    speech_config.speech_synthesis_voice_name = "en-IN-NeerjaNeural"
    speech_synthesizer = speechsdk.SpeechSynthesizer(
        speech_config=speech_config, audio_config=None)

    result = speech_synthesizer.speak_text_async(text).get()
    speech_synthesizer.stop_speaking()
    if result:
        if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
            audio_data = io.BytesIO()
            audio_data.write(result.audio_data)
            audio_data.seek(0)
            return audio_data
        else:
            raise Exception('TTS synthesis failed.')
    else:
        raise Exception('No result received from TTS service.')
