import os
from flask import Flask, render_template, request, jsonify, send_file
from .utils.audio_extractor import download_audio
from .utils.speech_to_text import transcribe_audio
from .utils.summarizer import summarize_text
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__, template_folder=os.path.abspath("templates"), static_folder=os.path.abspath("static"))
app.secret_key = os.getenv("SECRET_KEY")

# Define transcript storage directory
TRANSCRIPT_DIR = os.path.join(os.getcwd(), "transcripts")
os.makedirs(TRANSCRIPT_DIR, exist_ok=True)  # Ensure directory exists

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/summarize', methods=['POST'])
def summarize():
    youtube_url = request.form['youtube_url']
    audio_file = download_audio(youtube_url)
    language = request.form.get("language", "auto")
    transcription = transcribe_audio(audio_file, language=language)
    summary = summarize_text(transcription)
    
    return jsonify({'summary': summary})

@app.route('/transcript', methods=['POST'])
def get_transcript():
    youtube_url = request.form['youtube_url']
    audio_file = download_audio(youtube_url)
    transcript = transcribe_audio(audio_file)

    # Save transcript to a file instead of session
    transcript_path = os.path.join(TRANSCRIPT_DIR, "transcript.txt")
    with open(transcript_path, "w", encoding="utf-8") as f:
        f.write(transcript)

    return jsonify({'transcript': transcript})

# Function to generate and save a PDF file
def save_transcript_as_pdf():
    transcript_path = os.path.join(TRANSCRIPT_DIR, "transcript.txt")

    # Ensure transcript file exists
    if not os.path.exists(transcript_path):
        return None  # Return None if no transcript is available

    pdf_path = os.path.join(TRANSCRIPT_DIR, "transcript.pdf")
    c = canvas.Canvas(pdf_path, pagesize=letter)
    width, height = letter
    c.setFont("Helvetica", 12)

    # Title
    c.drawString(50, height - 50, "YouTube Video Transcript")

    # Read transcript from file
    with open(transcript_path, "r", encoding="utf-8") as f:
        transcript_text = f.read()

    # Define text wrapping parameters
    y_position = height - 70  # Start below the title
    left_margin = 50
    max_width = 90  # Max characters per line before wrapping

    # Wrap text manually using textwrap
    wrapped_lines = textwrap.wrap(transcript_text, width=max_width)

    for line in wrapped_lines:
        if y_position < 50:  # Create new page if out of space
            c.showPage()
            c.setFont("Helvetica", 12)
            y_position = height - 50

        c.drawString(left_margin, y_position, line)
        y_position -= 18  # Move down for the next line

    c.save()
    return pdf_path

# Function to return the saved transcript as a TXT file
def save_transcript_as_txt():
    transcript_path = os.path.join(TRANSCRIPT_DIR, "transcript.txt")
    if os.path.exists(transcript_path):
        return transcript_path  # Use existing file instead of session
    return None

@app.route('/download-transcript', methods=['GET'])
def download_transcript():
    format_type = request.args.get('format', 'txt')

    # Ensure transcript exists
    transcript_path = os.path.join(TRANSCRIPT_DIR, "transcript.txt")
    if not os.path.exists(transcript_path):
        return jsonify({"error": "Transcript not found. Please generate it first."}), 400

    if format_type == "pdf":
        file_path = save_transcript_as_pdf()
    else:
        file_path = save_transcript_as_txt()

    # Ensure the file exists before sending
    if file_path and os.path.exists(file_path):
        return send_file(file_path, as_attachment=True)
    else:
        return jsonify({"error": "Failed to generate transcript file."}), 500

if __name__ == '__main__':
    app.run(debug=True)
