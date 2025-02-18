import openai

def transcribe_audio(audio_file):
    openai.api_key = 'your-openai-api-key'
    with open(audio_file, 'rb') as file:
        transcription = openai.Audio.transcribe("whisper-1", file)
    return transcription['text']