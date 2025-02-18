import yt_dlp

def download_audio(youtube_url):
    ydl_opts = {
        'format': 'bestaudio/best',
        'ffmpeg_location': "C:/ProgramData/chocolatey/bin",  # Specify the location of ffmpeg and ffprobe
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': 'audio',  # Output file name
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([youtube_url])
    return 'audio.mp3'  # Return the downloaded file name
