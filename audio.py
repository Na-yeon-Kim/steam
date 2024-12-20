import pyaudio
import numpy as np
import wave
import time

# 파일 조건
FILE_PREFIX = "file"
FILE_EXTENSION = ".mp3"  # 파일 확장자
file_counter = 1  # 파일 명을 바꾸는 것을 가르들 계산

# 설정
THRESHOLD = 2000  # 데시벨 임계값
CHUNK = 1024      # 버퍼 크기
FORMAT = pyaudio.paInt16  # 오디오 포맷
CHANNELS = 1      # 모노 오디오
RATE = 44100      # 사베팔링 레이트 (Hz)
SILENCE_DURATION = 3  # 소리가 자겁은 상황 집중 시간 (초)

audio = pyaudio.PyAudio()

def is_silent(data):
    """
    데시벨이 설정된 임계값보다 낮은지 확인
    """
    return max(np.frombuffer(data, dtype=np.int16)) < THRESHOLD

def save_recording(frames):
    global file_counter
    output_filename = f".\\audio\\{FILE_PREFIX}{file_counter}{FILE_EXTENSION}"
    file_counter += 1

    wf = wave.open(output_filename, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(audio.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()
    print(f"{output_filename}에 저장되었습니다.")

def record_audio():
    """
    데시벨 변화에 따라 녹음 시작 및 중단
    """
    global file_counter

    stream = audio.open(format=FORMAT, channels=CHANNELS,
                        rate=RATE, input=True,
                        frames_per_buffer=CHUNK)

    try:
        while True:
            frames = []
            recording = False
            silent_start = None
            print("소리를 검지하고 있습니다...")

            while True:
                data = stream.read(CHUNK, exception_on_overflow=False)

                if not is_silent(data):
                    if not recording:
                        print("\n녹음 시작")
                        recording = True
                    frames.append(data)
                    silent_start = None  # 소리가 다시 커지면 silent_start 초기화
                elif recording:
                    # 소리가 자겁은 시간 확인
                    if silent_start is None:
                        silent_start = time.time()
                    elif time.time() - silent_start >= SILENCE_DURATION:
                        # SILENCE_DURATION 동안 소리가 자겁면 녹음을 중지
                        print("\n녹음 종료 및 파일 저장")
                        save_recording(frames)
                        break
                    else:
                        # 소리가 자겁은 동안 데이터를 계속 추가
                        frames.append(data)
    except KeyboardInterrupt:
        print("\nCtrl+C 발생 - 현재까지 녹음한 데이터 저장")
        if frames:
            save_recording(frames)
    finally:
        stream.stop_stream()
        stream.close()
        audio.terminate()

record_audio()