import os
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder, StandardScaler
import joblib

FOURIER_DIR = "fourier"

def load_fourier_dataset(fourier_dir=FOURIER_DIR):
    X, y = [], []
    for inst in os.listdir(fourier_dir):
        inst_path = os.path.join(fourier_dir, inst)
        if not os.path.isdir(inst_path):
            continue
        for file in os.listdir(inst_path):
            if file.endswith(".npy"):
                arr = np.load(os.path.join(inst_path, file))
                X.append(arr)
                y.append(inst)
    X = np.array(X)
    y = np.array(y)
    return X, y

# 데이터 불러오기
X, y = load_fourier_dataset()

print("데이터 크기:", X.shape, "라벨 개수:", len(set(y)))

# 라벨 인코딩
le = LabelEncoder()
y_encoded = le.fit_transform(y) # 악기 이름을 숫자로

# 스케일링
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X) # 표준화 작업업

# 모델 훈련 (랜덤포레스트)
clf = RandomForestClassifier(n_estimators=200, max_depth=20, random_state=42)
clf.fit(X_scaled, y_encoded)

# 성능 평가
train_acc = clf.score(X_scaled, y_encoded)
print(f"학습 정확도: {train_acc:.3f}")

# 모델 저장
os.makedirs("models", exist_ok=True)
joblib.dump(clf, "models/instrument_rf.pkl")
joblib.dump(le, "models/label_encoder.pkl")
joblib.dump(scaler, "models/scaler.pkl")
print("모델 저장 완료")
