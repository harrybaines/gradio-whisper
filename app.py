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

with gr.Blocks() as demo:
    url_input = gr.Textbox(placeholder='Youtube video URL', label='URL')
    transcribe_btn = gr.Button('Transcribe')
    gr.Examples(
        examples=["https://www.youtube.com/watch?v=ZgN7ZYUxcXM&ab_channel=LexClips"],
        inputs=url_input
    )
    transcribe_btn.click(convert, inputs=url_input, outputs=[gr.File()])

demo.launch()