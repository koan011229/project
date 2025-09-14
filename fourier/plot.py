import os
import random
import numpy as np
import matplotlib.pyplot as plt
import soundfile as sf

SAMPLE_RATE = 22050
DATASET_DIR = "dataset"

def plot_random_examples(dataset_dir=DATASET_DIR, sr=SAMPLE_RATE):
    instruments = [d for d in os.listdir(dataset_dir) if os.path.isdir(os.path.join(dataset_dir, d))]
    
    for inst in instruments:
        inst_path = os.path.join(dataset_dir, inst)
        wav_files = [f for f in os.listdir(inst_path) if f.endswith(".wav")]
        if not wav_files:
            continue

        # 랜덤 하나 선택
        file = random.choice(wav_files)
        wav_path = os.path.join(inst_path, file)

        signal, sr_file = sf.read(wav_path)
        if sr_file != sr:
            raise ValueError(f"샘플레이트 불일치: {sr_file} vs {sr}")

        # FFT 변환
        spectrum = np.fft.rfft(signal)
        freqs = np.fft.rfftfreq(len(signal), 1/sr)
        magnitude = np.abs(spectrum)

        # 시각화
        fig, axs = plt.subplots(2, 1, figsize=(10, 6))
        t = np.linspace(0, len(signal)/sr, num=len(signal))

        # 시간 도메인
        axs[0].plot(t, signal)
        axs[0].set_title(f"{inst} - Time Domain ({file})")
        axs[0].set_xlabel("Time [s]")
        axs[0].set_ylabel("Amplitude")

        # 주파수 도메인인
        axs[1].plot(freqs, magnitude)
        axs[1].set_xlim(0, 5000)
        axs[1].set_title(f"{inst} - Frequency Domain (FFT)")
        axs[1].set_xlabel("Frequency [Hz]")
        axs[1].set_ylabel("Magnitude")

        plt.tight_layout()
        plt.show()

plot_random_examples()
