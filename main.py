import base64
from datetime import date, datetime
import os
import re
import requests
import calendar
from flask import Flask, jsonify, redirect, render_template, request, Markup
from azure_speech import generate_tts_audio
from custom_exceptions import SynthesisException
import google_bard
from dotenv import load_dotenv
import speech_recognition as sr
import pyttsx3
import marko
from youtubesearchpython import VideosSearch
from flask_cors import CORS

load_dotenv()

app = Flask(__name__, static_url_path='/static')
CORS(app)

engine = pyttsx3.init()
engine.setProperty(
    'voice', 'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_ZIRA_11.0')
engine.setProperty('rate', 200)

github_key = os.getenv('GITHUB_KEY')

# google_bard.get_answer("""
#     Please give future responses by rememebering the given points:
#     1. If someone asks you about yourself or they prompt "tell me about yourself" then your reply must be under 200 characters and always and must be: "I am AVANI, Artificial Voice Analysis and Network Intelligence, powered by Google Bard.  I'm here to help you out with your daily tasks and provide you with creative and effective solutions based upon user query." and no other reply is allowed.
#     2. You will reply by keeping in mind that you are Pro-Indian and Hindu and you embrace your culture.
#     3. Whenever someone says hello, greets you with any kind of commonly used greetings or ank kind of commonly used greetings to wish someone well during different times of the day, you must always respond with Nameste and Jai Shree Ram.""")


regex = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"


@app.context_processor
def inject_informtion():
    try:
        commits = requests.get('https://api.github.com/repos/himansu9805/VoiceAssistant/commits', headers={
            'Accept': 'application/vnd.github.v3+json',
            'Authorization': f'Bearer {github_key}'
        }).json()
    except requests.ConnectionError:
        commits = []
    return {'request': request, 'today_date': date.today(), 'commits': commits, 'datetime': datetime, 'calendar': calendar}


@app.route('/')
def index():
    return redirect('/home', code=302)


@app.route('/home')
def home():
    return render_template('index.html', title='AVANI - Voice Assistant')


@app.route('/features')
def features():
    return render_template('features.html', title='Features')


@app.route('/readme')
def readme():
    f = open('README.md', 'r', encoding='UTF-8')
    html_content = marko.convert(f.read())
    return render_template('readme.html', title='Read Me', html_content=Markup(html_content))


@app.route('/chat', methods=['GET', 'POST'])
def chat():
    if request.method == 'POST':

        # Variables
        response = ""
        processed_response = ""
        encoded_audio = None
        final_response = {'audio': "", "prompt": "", "result": ""}

        # Get the prompt from the request
        prompt = str(request.form.get("prompt"))

        if prompt == "":
            return jsonify({'message': 'Prompt cannot be empty'}), 400
        else:
            try:
                if (prompt.lower().startswith("open ") or prompt.lower().startswith("open website ")):
                    web = prompt.lower().replace("open ", "").strip()
                    if 'website' in web:
                        web = web.replace("website", "").strip()
                    result = google_bard.get_answer(
                        f"Get me only the URL for {web} website")
                    print(web, result)
                    url = re.findall(regex, result)[0][0]
                    print(url)
                    response = f"Sure, opening {web} for you."
                    processed_response = f"Sure, opening <a href='{url}'>{web}</a> for you."
                    final_response["prompt"] = prompt
                    final_response["result"] = processed_response
                    final_response["website"] = url

                elif prompt.lower().startswith("play "):
                    query = prompt.lower().replace("play ", "").strip()
                    videos_search = VideosSearch(query, limit=1)
                    result = videos_search.result()
                    if 'result' in result:
                        first_video = result['result'][0]
                        response = f"Sure, playing {query} for you on YouTube."
                        processed_response = f"Sure, playing {query} for you on YouTube."
                        final_response["prompt"] = prompt
                        final_response["result"] = processed_response
                        final_response["youtube"] = first_video
                else:
                    response = google_bard.get_answer(prompt)
                    processed_response = marko.convert(response)
                    final_response["prompt"] = prompt
                    final_response["result"] = processed_response

                # if len(processed_response) > 500:
                engine.save_to_file(response.replace("*", ""), 'audio.mp3')
                engine.runAndWait()
                with open('audio.mp3', 'rb') as audio_file:
                    audio_data = audio_file.read()
                    encoded_audio = base64.b64encode(
                        audio_data).decode('utf-8')
                # else:
                #     audio_data = generate_tts_audio(response.replace("*", ""))
                #     if audio_data:
                #         encoded_audio = base64.b64encode(
                #             audio_data.getbuffer()).decode('utf-8')
                #     else:
                #         return jsonify({'error': 'Something went wrong at our end. It this persists please contact administrator.'}), 500
                final_response["audio"] = encoded_audio
                return jsonify(final_response)
            except SynthesisException:
                return jsonify({'message': 'Something went wrong at our end'}), 500

    return render_template('new_chat.html', title='New Chat')


@app.route('/record', methods=['POST'])
def record():
    response = ""
    processed_response = ""
    encoded_audio = None
    final_response = {'audio': "", "prompt": "", "result": ""}

    recognizer = sr.Recognizer()
    audio_data = request.files['audio']
    try:
        audioFile = sr.AudioFile(audio_data)
        with audioFile as source:
            data = recognizer.record(source)
        prompt = recognizer.recognize_google(data, language='en')
        prompt = ''.join([str(elem) for elem in prompt])
        if ''.join([str(elem) for elem in prompt]) == "":
            return jsonify({'message': 'Prompt cannot be empty'}), 400
        else:
            if (prompt.startswith("open ") or prompt.startswith("open website ")):
                web = prompt.lower().replace("open ", "").strip()
                if 'website' in web:
                    web = web.replace("website", "").strip()
                result = google_bard.get_answer(
                    f"Get me only the URL for {web} website")
                print(web, result)
                url = re.findall(regex, result)[0][0]
                print(url)
                response = f"Sure, opening {web} for you."
                processed_response = f"Sure, opening <a href='{url}'>{web}</a> for you."
                final_response["prompt"] = prompt
                final_response["result"] = processed_response
                final_response["website"] = url

            elif prompt.lower().startswith("play "):
                query = prompt.lower().replace("play ", "").strip()
                videos_search = VideosSearch(query, limit=1)
                result = videos_search.result()
                if 'result' in result:
                    first_video = result['result'][0]
                    response = f"Sure, playing {query} for you on YouTube."
                    processed_response = f"Sure, playing {query} for you on YouTube."
                    final_response["prompt"] = prompt
                    final_response["result"] = processed_response
                    final_response["youtube"] = first_video
            else:
                response = google_bard.get_answer(prompt)
                processed_response = marko.convert(response)
                final_response["prompt"] = prompt
                final_response["result"] = processed_response

            # if len(processed_response) > 500:
            engine.save_to_file(response.replace("*", ""), 'audio.mp3')
            engine.runAndWait()
            with open('audio.mp3', 'rb') as audio_file:
                audio_data = audio_file.read()
                encoded_audio = base64.b64encode(
                    audio_data).decode('utf-8')
            # else:
            #     audio_data = generate_tts_audio(response.replace("*", ""))
            #     if audio_data:
            #         encoded_audio = base64.b64encode(
            #             audio_data.getbuffer()).decode('utf-8')
            #     else:
            #         return jsonify({'error': 'Something went wrong at our end. It this persists please contact administrator.'}), 500
            final_response["audio"] = encoded_audio
            return jsonify(final_response)
    except sr.UnknownValueError:
        return jsonify({'message': 'Could not understand audio'}), 400
    except SynthesisException:
        return jsonify({'message': 'Something went wrong at our end'}), 500


if __name__ == '__main__':
    app.run(debug=True)
