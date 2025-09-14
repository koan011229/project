import os
import numpy as np
import soundfile as sf
from sklearn.model_selection import train_test_split

SAMPLE_RATE = 22050
DATASET_DIR = "dataset"
FOURIER_TRAIN_DIR = "fourier"
FOURIER_TEST_DIR = "fourier_test"

os.makedirs(FOURIER_TRAIN_DIR, exist_ok=True)
os.makedirs(FOURIER_TEST_DIR, exist_ok=True)

def compute_fft(wav_path): # Fast Fourier Transform 적용
    signal, sr = sf.read(wav_path)
    if sr != SAMPLE_RATE: # 예외 표시
        raise ValueError(f"샘플레이트 불일치: {sr}Hz (기대값 {SAMPLE_RATE}Hz)")
    spectrum = np.fft.rfft(signal)
    magnitude = np.abs(spectrum)
    return magnitude.astype(np.float32)

def convert_dataset_to_fourier(dataset_dir=DATASET_DIR, 
                               out_train=FOURIER_TRAIN_DIR, 
                               out_test=FOURIER_TEST_DIR,
                               test_size=0.2, random_state=42):
    for inst in os.listdir(dataset_dir):
        inst_path = os.path.join(dataset_dir, inst)
        if not os.path.isdir(inst_path):
            continue

        # 악기별 output 폴더 생성
        inst_out_train = os.path.join(out_train, inst)
        inst_out_test = os.path.join(out_test, inst)
        os.makedirs(inst_out_train, exist_ok=True)
        os.makedirs(inst_out_test, exist_ok=True)

        # wav 파일 모으기
        wav_files = [f for f in os.listdir(inst_path) if f.endswith(".wav")]

        # 훈련용 테스트용 분할
        train_files, test_files = train_test_split(
            wav_files, test_size=test_size, random_state=random_state
        )

        # 훈련용용 변환
        for file in train_files:
            wav_path = os.path.join(inst_path, file)
            mag = compute_fft(wav_path)
            base = os.path.splitext(file)[0]
            out_path = os.path.join(inst_out_train, base + ".npy")
            np.save(out_path, mag)
            print(f"훈련용 저장: {out_path}")

        # 테스트용용 변환
        for file in test_files:
            wav_path = os.path.join(inst_path, file)
            mag = compute_fft(wav_path)
            base = os.path.splitext(file)[0]
            out_path = os.path.join(inst_out_test, base + ".npy")
            np.save(out_path, mag)
            print(f"테스트용용 저장: {out_path}")

# 실행
convert_dataset_to_fourier()
