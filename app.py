import gradio as gr
from pytube import YouTube
import whisper
import torch
import os

YT_MAX_MINS = 3600
OUTPUT_DIR = './outputs'
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
model = whisper.load_model("base", device=DEVICE)

def transcribe(filepath):
    result = model.transcribe(filepath)
    os.remove(filepath)
    transcription = result['text'].strip()
    filename = f'{OUTPUT_DIR}/transcription.txt'
    with open(filename, 'w') as f:
        f.write(transcription)
    return filename
    
def download_video(url):    
    try:
        yt = YouTube(url)
        if yt.length > YT_MAX_MINS:
            raise gr.Error("Video length limited to 1 hour")
        video = yt.streams.filter(only_audio=True).first()
        return video.download(output_path=OUTPUT_DIR)
    except Exception as e:
        raise gr.Error("Error downloading video. Please check the URL.")
    
def convert(url):
    filepath = download_video(url)
    return transcribe(filepath)

demo = gr.Interface(fn=convert, inputs="text", outputs="file", allow_flagging=False)
demo.launch()

# About 15 secs for a 5 minute video