from datetime import date, datetime
import requests
import calendar
from flask import Flask, redirect, render_template, request
import chatGPT

app = Flask(__name__, static_url_path='/static')


@app.context_processor
def inject_informtion():
    try:
        commits = requests.get('https://api.github.com/repos/himansu9805/the-microblogging-project/commits', headers={
            'Accept': 'application/vnd.github.v3+json',
            'Authorization': 'Bearer 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'
        }).json()
    except requests.ConnectionError:
        commits = []
    return {'today_date': date.today(), 'commits': commits, 'datetime': datetime, 'calendar': calendar}


@app.route('/')
def index():
    return redirect('/home', code=302)


@app.route('/home')
def home():
    return render_template('index.html', title='AVANI - Voice Assistant')


@app.route('/chat', methods=['GET', 'POST'])
def chat():
    if request.method == 'POST':
        prompt = request.form.get("prompt")
        response = chatGPT.generate_response(prompt)
        chat_title = chatGPT.generate_response(
            f"Please generate a title for this response: {response}")
        return {"chat_title": chat_title, "result": response}
    return render_template('new_chat.html', title='New Chat')
