import os
from flask import Flask, render_template, request, jsonify, send_file, session
from .utils.audio_extractor import download_audio
from .utils.speech_to_text import transcribe_audio
from .utils.summarizer import summarize_text
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import simpleSplit
from dotenv import load_dotenv


app = Flask(__name__, template_folder=os.path.abspath("templates"), static_folder=os.path.abspath("static"))
app.secret_key = os.getenv("SECRET_KEY")

TRANSCRIPT_DIR = os.path.join(os.getcwd(), "transcripts")
os.makedirs(TRANSCRIPT_DIR, exist_ok=True)  

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

    session['transcript'] = transcript  # Stores transcript in session
    return jsonify({'transcript': transcript})

# Function to generate and save a PDF file
def save_transcript_as_pdf(transcript_text):
    filename = os.path.join(TRANSCRIPT_DIR, "transcript.pdf")

    try:
        pdf_canvas = canvas.Canvas(filename, pagesize=letter)
        pdf_canvas.setFont("Helvetica", 12)

        width, height = letter

        pdf_canvas.drawString(100, height - 50, "Transcript:")

        y_position = height - 70  

        max_width = 450  

        lines = transcript_text.split("\n")  

        for line in lines:
            wrapped_text = simpleSplit(line, "Helvetica", 12, max_width)  
            for sub_line in wrapped_text:
                if y_position < 50:  
                    pdf_canvas.showPage()
                    pdf_canvas.setFont("Helvetica", 12)
                    y_position = height - 50  

                pdf_canvas.drawString(50, y_position, sub_line)  
                y_position -= 20  

        pdf_canvas.save()  
        return filename
    except Exception as e:
        print(f"Error generating PDF: {e}")
        return None  # Returns None if PDF creation fail

# Function to generate and save a TXT file
def save_transcript_as_txt(transcript_text):
    filename = os.path.join(TRANSCRIPT_DIR, "transcript.txt")
    with open(filename, "w", encoding="utf-8") as f:
        f.write(transcript_text)
    return filename

@app.route('/download-transcript', methods=['GET'])
def download_transcript():
    format_type = request.args.get('format', 'txt')

    # Retrieves transcript from session
    transcript_text = session.get('transcript', None)
    if not transcript_text:
        return jsonify({"error": "Transcript not found. Please generate it first."}), 400

    if format_type == "pdf":
        file_path = save_transcript_as_pdf(transcript_text)
    else:
        file_path = save_transcript_as_txt(transcript_text)

    return send_file(file_path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
