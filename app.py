import streamlit as st
import os
from pathlib import Path
from zipfile import ZipFile
from dotenv import load_dotenv
from pytube import YouTube
import openai

# Load environment variables from .env file
load_dotenv()

# Set the OpenAI API key
api_key = st.sidebar.text_input('Enter your OpenAI API key:', type='password')

# Check if API key is provided
if not api_key:
    st.sidebar.warning('Please enter your OpenAI API key in the sidebar.')
else:
    openai.api_key = api_key  # Set the API key for OpenAI

    @st.cache
    def load_model():
        # Replace 'whisper' with the actual library you are using for loading the model
        model = whisper.load_model("base")
        return model

    def save_audio(url):
        yt = YouTube(url)
        video = yt.streams.filter(only_audio=True).first()
        out_file = video.download()
        base, ext = os.path.splitext(out_file)
        file_name = base + '.mp3'
        try:
            os.rename(out_file, file_name)
        except WindowsError:
            os.remove(file_name)
            os.rename(out_file, file_name)
        audio_filename = Path(file_name).stem+'.mp3'
        st.success(yt.title + " has been successfully downloaded")
        return yt.title, audio_filename

    def audio_to_transcript(audio_file):
        model = load_model()
        result = model.transcribe(audio_file)
        transcript = result["text"]
        return transcript

    def text_to_news_article(text):
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt="Write a news article in 500 words from the below text:\n"+text,
            temperature=0.7,
            max_tokens=600,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )
        return response['choices'][0]['text']

    st.markdown('# 📝 **News Article Generator App**')

    st.sidebar.header('API Configuration')
    st.sidebar.info("Provide your OpenAI API key to use the app.")

    st.header('Input the Video URL')
    url_link = st.text_input('Enter URL of YouTube video:')

    if st.checkbox('Start Analysis'):
        video_title, audio_filename = save_audio(url_link)
        st.audio(audio_filename)
        transcript = audio_to_transcript(audio_filename)
        st.header("Transcript is getting generated...")
        st.success(transcript)
        st.header("News Article")
        result = text_to_news_article(transcript)
        st.success(result)
        
        # Save the files
        transcript_txt = open('transcript.txt', 'w')
        transcript_txt.write(transcript)
        transcript_txt.close()  
        
        article_txt = open('article.txt', 'w')
        article_txt.write(result) 
        article_txt.close() 
        
        zip_file = ZipFile('output.zip', 'w')
        zip_file.write('transcript.txt')
        zip_file.write('article.txt')
        zip_file.close()
        
        with open("output.zip", "rb") as zip_download:
            btn = st.download_button(
                label="Download ZIP",
                data=zip_download,
                file_name="output.zip",
                mime="application/zip"
            )

