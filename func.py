import pyaudio
import keyboard
import io
import wave


def recording():
    # 설정
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 44100
    CHUNK = 1024

    # pyaudio 객체 생성
    audio = pyaudio.PyAudio()

    # 녹음할 준비
    frames = []
    
    print("Press 'r' to start recording.")
    keyboard.wait('r')  # 'r' 키 입력 대기
    
    stream = audio.open(format=FORMAT, channels=CHANNELS,
                        rate=RATE, input=True,
                        frames_per_buffer=CHUNK)
    print("Recording... Press 's' to stop.")
    while True:
        if keyboard.is_pressed('s'):
            print("Stopped recording.")
            break
        data = stream.read(CHUNK)
        frames.append(data)

    stream.stop_stream()
    stream.close()
    
    buffer = io.BytesIO()
    waveFile = wave.open(buffer, 'wb')
    waveFile.setnchannels(CHANNELS)
    waveFile.setsampwidth(audio.get_sample_size(FORMAT))
    waveFile.setframerate(RATE)
    waveFile.writeframes(b''.join(frames))
    waveFile.close()
    buffer.seek(0)

    return buffer.getvalue()