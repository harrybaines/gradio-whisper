import gradio as gr
from pytube import YouTube
import whisper
import torch
import os

YT_MAX_MINS = 3600
OUTPUT_DIR = './outputs'
MODEL_SIZES = list(whisper._MODELS.keys())

DEVICE = "cuda" if torch.cuda.is_available() else "cpu"


def transcribe(filepath, model):
    result = model.transcribe(filepath)
    os.remove(filepath)
    transcription = result['text'].strip()
    filename = f'{OUTPUT_DIR}/transcription.txt'
    with open(filename, 'w') as f:
        f.write(transcription)
    return transcription, filename
    
def download_video(url):    
    try:
        yt = YouTube(url)
        if yt.length > YT_MAX_MINS:
            raise gr.Error("Video length limited to 1 hour")
        video = yt.streams.filter(only_audio=True).first()
        return video.download(output_path=OUTPUT_DIR)
    except Exception as e:
        raise gr.Error("Error downloading video. Please check the URL.")
    
def run(url, model_size):
    filepath = download_video(url)
    model = whisper.load_model(model_size, device=DEVICE)
    transcription, filename = transcribe(filepath, model)
    return transcription, filename

with gr.Blocks() as interface:
    gr.Markdown(
        """
        # OpenAI Whisper Demo for YouTube Videos
        Note: tiny model takes about 12 seconds to transcribe a 5 minute video.
        """
    )
    with gr.Row():
        url_input = gr.Textbox(placeholder='Youtube video URL', label='URL')
        model_size = gr.Dropdown(choices=MODEL_SIZES, value='tiny', label="Model")

    gr.Examples(
        examples=[
            "https://www.youtube.com/watch?v=ZgN7ZYUxcXM&ab_channel=LexClips",
            "https://www.youtube.com/shorts/ZlUj2WQ7_GE"
        ],
        inputs=url_input
    )
    transcribe_btn = gr.Button('Transcribe')
    
    with gr.Row():    
        output_transcript = gr.Textbox(lines=10, placeholder='Transcription of the video', label='Transcription')
        transcribe_btn.click(
            run,
            inputs=[url_input, model_size],
            outputs=[output_transcript, gr.File()]
        )
    

interface.launch()