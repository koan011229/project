import os
import random
import numpy as np
import joblib

FOURIER_DIR = "fourier_test"

clf = joblib.load("models/instrument_rf.pkl")
scaler = joblib.load("models/scaler.pkl")
le = joblib.load("models/label_encoder.pkl")

# 악기 목록
instruments = [d for d in os.listdir(FOURIER_DIR) if os.path.isdir(os.path.join(FOURIER_DIR, d))]
instruments.sort()

while True:
    print("\n테스트할 악기를 선택하세요:")
    print("0. 종료")
    for idx, inst in enumerate(instruments, start=1):
        print(f"{idx}. {inst}")

    try:
        choice = int(input("번호 입력: ").strip())
    except ValueError:
        print("숫자를 입력하세요")
        continue

    if choice == 0:
        print("테스트 종료!")
        break

    if choice < 1 or choice > len(instruments):
        print("잘못된 번호입니다!")
        continue

    inst = instruments[choice - 1]

    # 랜덤으로 악기 하나 선택
    files = [f for f in os.listdir(os.path.join(FOURIER_DIR, inst)) if f.endswith(".npy")]
    if not files:
        print("npy 파일이 없습니다")
        continue

    file = random.choice(files)
    path = os.path.join(FOURIER_DIR, inst, file)
    print(f"선택된 파일: {file}")

    # 데이터 변환
    X = np.load(path).reshape(1, -1)
    X_scaled = scaler.transform(X)

    # 모델 예측
    pred = clf.predict(X_scaled)[0]
    pred_name = le.inverse_transform([pred])[0]
    proba = clf.predict_proba(X_scaled)[0]

    # 출력
    print("\n예측 결과")
    print(f"정답: {inst}")
    print(f"예측: {pred_name} {'O' if inst == pred_name else 'X'}")
    print("모든 클래스 확률:")
    for name, p in zip(le.classes_, proba):
        print(f"  {name}: {p*100:.1f}%")
