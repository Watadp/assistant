import speech_recognition as sr
import pyaudio
import wave
import os

directory = "../assets/voice_search_cache/"
input_file = directory + "data_audio.wav"

recognizer = sr.Recognizer()

def record_audio(input_file, duration=8, samplerate=44100):
    print("Recording...")
    chunk = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 44100

    p = pyaudio.PyAudio()

    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=chunk)

    frames = []

    for i in range(0, int(RATE / chunk * duration)):
        data = stream.read(chunk)
        frames.append(data)

    stream.stop_stream()
    stream.close()
    p.terminate()

    wf = wave.open(input_file, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()
    print(f"Audio recorded and saved at {input_file}")

def transcribe_multilanguage(input_file):
    # Nhận diện giọng nói từ file âm thanh sử dụng thư viện SpeechRecognition
    with sr.AudioFile(input_file) as source:
        audio = recognizer.record(source)

    # Nhận dạng ngôn ngữ đa ngôn ngữ
    try:
        # Danh sách ngôn ngữ có thể xuất hiện trong câu nói
        languages = "vi-VN,en-US,"  # Sử dụng chuỗi duy nhất thay vì danh sách

        # Nhận dạng
        text = recognizer.recognize_google(audio, language=languages)

        print("Text:", text)
    except sr.UnknownValueError:
        print("Could not understand the audio")
    except sr.RequestError as e:
        print("Error:", str(e))

def process_cycle(input_file):
    record_audio(input_file)
    transcribe_multilanguage(input_file)
    os.remove(input_file)

process_cycle(input_file)