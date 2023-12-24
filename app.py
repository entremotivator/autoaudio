import streamlit as st
import numpy as np
import wave
import speech_recognition as sr
import io
import base64

def main():
    st.title("Streamlit Audio Recorder")

    # Function to capture audio and display a plot
    def capture_audio():
        recognizer = sr.Recognizer()

        st.write("Recording...")

        # Use the default microphone as the audio source
        with sr.Microphone() as source:
            audio_data = recognizer.listen(source, timeout=5)

        st.write("Recording complete!")

        # Save the recorded audio to a WAV file
        save_audio(audio_data)

        # Convert the audio data to text using SpeechRecognition
        try:
            text = recognizer.recognize_google(audio_data)
            st.write("Transcription:")
            st.write(text)
        except sr.UnknownValueError:
            st.write("Speech Recognition could not understand audio")
        except sr.RequestError as e:
            st.write(f"Could not request results from Google Speech Recognition service; {e}")

    # Function to save recorded audio to a WAV file
    def save_audio(audio_data):
        with open("recorded_audio.wav", "wb") as audio_file:
            audio_file.write(audio_data.get_wav_data())

        st.write("Audio saved to recorded_audio.wav")

        # Provide a download link for the saved audio file
        with open("recorded_audio.wav", "rb") as audio_file:
            audio_bytes = audio_file.read()
            st.audio(audio_bytes, format="audio/wav", start_time=0)

    # Button to start capturing audio
    if st.button("Start Audio Capture"):
        capture_audio()

if __name__ == "__main__":
    main()
