import os
import numpy as np
import soundfile as sf

SAMPLE_RATE = 44100
DURATION = 2.0
DATASET_DIR = "dataset"

os.makedirs(DATASET_DIR, exist_ok=True)

def midi_to_freq(note):
    return 440.0 * (2.0 ** ((note - 69) / 12.0))

def synthesize_wave(note, instrument_name="piano", duration=DURATION, sr=SAMPLE_RATE):
    freq = midi_to_freq(note)
    t = np.linspace(0, duration, int(sr * duration), endpoint=False)

    if instrument_name == "piano":
        signal = np.sin(2 * np.pi * freq * t)
        for h in range(2, 5):
            signal += (0.5 / h) * np.sin(2 * np.pi * freq * h * t)
        signal *= np.exp(-3 * t) 
    elif instrument_name == "violin":
        vibrato = 0.1 * np.sin(2 * np.pi * 6 * t) 
        signal = np.sin(2 * np.pi * freq * t + vibrato)
        signal += 0.3 * np.sin(2 * np.pi * 2 * freq * t)
    elif instrument_name == "drum":
        kick = 0.8 * np.sin(2 * np.pi * 60 * t) * np.exp(-t * 8)
        snare = 0.6 * np.sin(2 * np.pi * 200 * t) * np.exp(-t * 10)
        snare += 0.3 * np.random.normal(0, 1, len(t)) * np.exp(-t * 12)
        hihat = 0.3 * np.sin(2 * np.pi * 8000 * t) * np.exp(-t * 15)
        signal = kick + snare + hihat
    elif instrument_name == "guitar":
        signal = np.sin(2 * np.pi * freq * t)
        signal += 0.3 * np.sin(2 * np.pi * 2 * freq * t)
        signal += 0.2 * np.sin(2 * np.pi * 3 * freq * t)
        signal *= np.exp(-2 * t)
    elif instrument_name == "flute":
        signal = np.sin(2 * np.pi * freq * t)
        signal += 0.05 * np.random.normal(0, 1, len(t)) * np.exp(-t * 3)
    else:
        signal = np.sin(2 * np.pi * freq * t)

    # 정규화
    signal = signal / np.max(np.abs(signal))
    return signal.astype(np.float32)

def save_dataset(instruments, notes_per_instrument=32, start_note=60):
    for inst in instruments:
        inst_folder = os.path.join(DATASET_DIR, inst)
        os.makedirs(inst_folder, exist_ok=True)
        for i in range(notes_per_instrument):
            note = start_note + i
            signal = synthesize_wave(note, instrument_name=inst)
            filename = os.path.join(inst_folder, f"note_{note}.wav")
            sf.write(filename, signal, SAMPLE_RATE)
            print(f"생성 완료: {filename}")

instruments = ["piano", "violin", "drum", "guitar", "flute"]
save_dataset(instruments, notes_per_instrument=32, start_note=60)
