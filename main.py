""" Main file for PottyPot """
#import speech_recognition as sr
from google.cloud import speech
from google.cloud.speech import enums, types
import pyaudio
import wave
import io
import os

client = speech.SpeechClient()

def record_audio():
    # We call this function in a loop so that every whatever seconds we clobber file.wav
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 16000
    CHUNK = 1024
    RECORD_SECONDS = 5
    WAVE_OUTPUT_FILENAME = "file.wav"
    audio = pyaudio.PyAudio()
    # start Recording
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

    waveFile = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    waveFile.setnchannels(CHANNELS)
    waveFile.setsampwidth(audio.get_sample_size(FORMAT))
    waveFile.setframerate(RATE)
    waveFile.writeframes(b''.join(frames))
    waveFile.close()
    print("Recording done :)")

def speech_detect():
    # We take the speech from record_audio() and shit it into google cloud.
    file_name = os.path.join(
        os.path.dirname(__file__),
        'file.wav')
    with io.open(file_name, 'rb') as audio_file:
        content = audio_file.read()
        audio = types.RecognitionAudio(content=content)
    config = types.RecognitionConfig(
        encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code='en-US')
    print("Tryna talk to google...")
    response = client.recognize(config, audio)
    for result in response.results:
        print('Transcript: {}'.format(result.alternatives[0].transcript))

def main():
    print("Welcome to PottyPot!")
    while True:
        record_audio()
        speech_detect()

if __name__ == "__main__":
    main()