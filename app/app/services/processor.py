import fitz  # PyMuPDF
import pytesseract
from PIL import Image
import whisper
import yt_dlp
import os

class InputProcessor:
    def __init__(self):
        # Load whisper model once (or lazy load)
        self.whisper_model = whisper.load_model("base")

    def process_pdf(self, file_path: str) -> str:
        """Extract text from PDF textbooks."""
        doc = fitz.open(file_path)
        text = ""
        for page in doc:
            text += page.get_text()
        return text

    def process_image(self, file_path: str) -> str:
        """OCR for scanned notes/images."""
        img = Image.open(file_path)
        text = pytesseract.image_to_string(img)
        return text

    def process_audio(self, file_path: str) -> str:
        """Transcribe audio lectures."""
        result = self.whisper_model.transcribe(file_path)
        return result["text"]

    def process_youtube(self, url: str) -> str:
        """Download audio from YT and transcribe."""
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': 'temp_audio.%(ext)s',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
            }],
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        
        text = self.process_audio("temp_audio.mp3")
        os.remove("temp_audio.mp3")
        return text

    def auto_process(self, file_path: str, file_type: str) -> str:
        if file_type == 'pdf':
            return self.process_pdf(file_path)
        elif file_type in ['png', 'jpg', 'jpeg']:
            return self.process_image(file_path)
        elif file_type in ['mp3', 'wav', 'm4a']:
            return self.process_audio(file_path)
        else:
            raise ValueError("Unsupported file format")
