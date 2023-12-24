import streamlit as st
import pyaudio
import numpy as np
import wave
import io
import base64

def main():
    st.title("Streamlit Audio Recorder")

    # Function to capture audio and display a plot
    def capture_audio():
        p = pyaudio.PyAudio()

        # Open a stream
        stream = p.open(format=pyaudio.paInt16,
                        channels=1,
                        rate=44100,
                        input=True,
                        frames_per_buffer=1024)

        st.write("Recording...")

        # Collect audio data for a few seconds
        frames = []
        for _ in range(5 * int(44100 / 1024)):  # Adjust the number of seconds as needed
            data = stream.read(1024)
            frames.append(np.frombuffer(data, dtype=np.int16))

        # Close the stream
        stream.stop_stream()
        stream.close()
        p.terminate()

        st.write("Recording complete!")

        # Display audio plot
        st.line_chart(np.concatenate(frames, axis=0))

        # Save the recorded audio to a WAV file
        save_audio(frames)

    # Function to save recorded audio to a WAV file
    def save_audio(frames):
        p = pyaudio.PyAudio()
        wf = wave.open("recorded_audio.wav", "wb")
        wf.setnchannels(1)
        wf.setsampwidth(p.get_sample_size(pyaudio.paInt16))
        wf.setframerate(44100)
        wf.writeframes(b"".join(frames))
        wf.close()

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
