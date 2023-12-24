import streamlit as st
import pyaudio
import numpy as np

def main():
    st.title("Streamlit App with PyAudio")

    # Function to capture audio and display a plot
    def capture_audio():
        p = pyaudio.PyAudio()

        # Open a stream
        stream = p.open(format=pyaudio.paInt16,
                        channels=1,
                        rate=44100,
                        input=True,
                        frames_per_buffer=1024)

        st.write("Listening...")

        # Collect audio data for a few seconds
        frames = []
        for _ in range(5 * int(44100 / 1024)):  # Adjust the number of seconds as needed
            data = stream.read(1024)
            frames.append(np.frombuffer(data, dtype=np.int16))

        # Close the stream
        stream.stop_stream()
        stream.close()
        p.terminate()

        # Display audio plot
        st.line_chart(np.concatenate(frames, axis=0))

    # Button to start capturing audio
    if st.button("Start Audio Capture"):
        capture_audio()

if __name__ == "__main__":
    main()
