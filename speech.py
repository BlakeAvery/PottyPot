#import speech_recognition as sr
from google.cloud import speech
from google.cloud.speech import enums, types
import pyaudio
import wave
import io
import os

def record_audio(seconds, filename="file.wav"):
    # We call this function in a loop so that every whatever seconds we clobber file.wav
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 16000
    CHUNK = 1024
    RECORD_SECONDS = seconds
    WAVE_OUTPUT_FILENAME = filename
    audio = pyaudio.PyAudio()
    # start Recording
    print(f"Starting audio recording for {RECORD_SECONDS} seconds...")
    stream = audio.open(format=FORMAT, channels=CHANNELS,
                        rate=RATE, input=True,
                        frames_per_buffer=CHUNK)
    frames = []

    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)
    # stop Recording
    stream.stop_stream()
    stream.close()
    audio.terminate()
    print("Recording done.")

    print(f"Saving file to {WAVE_OUTPUT_FILENAME}...")
    waveFile = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    waveFile.setnchannels(CHANNELS)
    waveFile.setsampwidth(audio.get_sample_size(FORMAT))
    waveFile.setframerate(RATE)
    waveFile.writeframes(b''.join(frames))
    waveFile.close()
    print("File saved.")

    return WAVE_OUTPUT_FILENAME


def speech_detect(filename):
    """ Send wav file to Google Cloud Speech API """
    # TODO: Fix and add comments
    client = speech.SpeechClient()

    # We take the speech from record_audio() and shit it into google cloud.

    print(f"Opening wav file: {filename}")
    file_path = os.path.join(
        os.path.dirname(__file__),
        filename)

    with io.open(file_path, 'rb') as audio_file:
        content = audio_file.read()
        audio = types.RecognitionAudio(content=content)
        config = types.RecognitionConfig(
            encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
            sample_rate_hertz=16000,
            language_code='en-US'
        )

    print(f"Sending {file_path} to Google...")
    response = client.recognize(config, audio)
    results = []
    for result in response.results:
        results.append(result.alternatives[0].transcript)
        print(results[0])
        #print(f"Transcript: {result.alternatives[0].transcript}")
    return results
