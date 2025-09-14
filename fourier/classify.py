import os
import numpy as np
import joblib
import matplotlib.pyplot as plt
from sklearn.metrics import classification_report, confusion_matrix, ConfusionMatrixDisplay

clf = joblib.load("models/instrument_rf.pkl")
scaler = joblib.load("models/scaler.pkl")
le = joblib.load("models/label_encoder.pkl")

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
    return np.array(X), np.array(y)

X, y = load_fourier_dataset()
y_encoded = le.transform(y)
X_scaled = scaler.transform(X)

y_pred = clf.predict(X_scaled)

report = classification_report(y_encoded, y_pred, target_names=le.classes_)
print(report)

cm = confusion_matrix(y_encoded, y_pred)
disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=le.classes_)

fig, ax = plt.subplots(figsize=(6, 6))
disp.plot(cmap=plt.cm.Blues, ax=ax, xticks_rotation=45, colorbar=False)
plt.title("악기별 혼동 행렬")
plt.show()

accuracies = cm.diagonal() / cm.sum(axis=1)
plt.figure(figsize=(8, 5))
plt.bar(le.classes_, accuracies, color="skyblue")
plt.ylim(0, 1)
plt.ylabel("Accuracy")
plt.title("악기별 정확도")
plt.show()
