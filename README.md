---
title: gradio-whsiper
emoji: 📹
colorFrom: red
colorTo: white
sdk: gradio
sdk_version: 3.8.2
app_file: app.py
pinned: false
---

# Whisper model for transcribing YouTube videos (on Gradio)

Transcribe a YouTube video URL to text using the OpenAI Whisper model.

On an M2 Pro MacBook Pro with the `tiny` model, transcribing a 5 minute video takes about 12 seconds.

View the [live site on HuggingFace](https://huggingface.co/spaces/harryb0905/gradio-whisper-yt-transcripts), or run the app locally on your machine:

```bash
virtualenv venv --python=3.9
source venv/bin/activate
pip install -r requirements.txt
gradio app.py
```

Then visit localhost:7860 in your browser.

![video](./docs/video.gif)

