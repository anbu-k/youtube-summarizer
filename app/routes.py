import os
from flask import Flask, render_template, request, jsonify
from .utils.audio_extractor import download_audio
from .utils.speech_to_text import transcribe_audio
from .utils.summarizer import summarize_text

app = Flask(__name__, template_folder=os.path.abspath("templates"), static_folder=os.path.abspath("static"))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/summarize', methods=['POST'])
def summarize():
    youtube_url = request.form['youtube_url']
    audio_file = download_audio(youtube_url)
    transcription = transcribe_audio(audio_file)
    summary = summarize_text(transcription)
    return jsonify({'summary': summary})

if __name__ == '__main__':
    app.run(debug=True)