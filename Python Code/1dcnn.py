import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from tensorflow.keras.utils import to_categorical

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv1D, MaxPooling1D, Dense, Dropout, Flatten
from sklearn.metrics import confusion_matrix, classification_report

# -----------------------------
# LOAD DATASET (CSV)
# -----------------------------
csv_path = r"C:\Users\anchi\OneDrive\Desktop\PYTHON PROGRAM\Project-Code\Segmented_Signals\Segmented_Beats_Balanced.csv"

df = pd.read_csv(csv_path)

# -----------------------------
# SEPARATE FEATURES & LABELS
# -----------------------------
# Assuming last column is label
X = df.iloc[:, :-1].values   # ECG signals
y = df.iloc[:, -1].values    # labels

# -----------------------------
# ENCODE LABELS
# -----------------------------
le = LabelEncoder()
y_encoded = le.fit_transform(y)
y_categorical = to_categorical(y_encoded)

# -----------------------------
# TRAIN-TEST SPLIT
# -----------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X, y_categorical, test_size=0.2, random_state=42
)

# -----------------------------
# RESHAPE FOR 1D CNN
# -----------------------------
X_train = X_train.reshape(-1, X_train.shape[1], 1)
X_test = X_test.reshape(-1, X_test.shape[1], 1)

# -----------------------------
# MODEL BUILDING (1D CNN)
# -----------------------------
model = Sequential([
    Conv1D(32, kernel_size=5, activation='relu', input_shape=(X_train.shape[1], 1)),
    MaxPooling1D(pool_size=2),

    Conv1D(64, kernel_size=5, activation='relu'),
    MaxPooling1D(pool_size=2),

    Flatten(),
    Dense(128, activation='relu'),
    Dropout(0.5),

    Dense(y_train.shape[1], activation='softmax')
])

model.compile(
    optimizer='adam',
    loss='categorical_crossentropy',
    metrics=['accuracy']
)

model.summary()

# -----------------------------
# TRAIN MODEL
# -----------------------------
history = model.fit(
    X_train, y_train,
    epochs=40,
    batch_size=64,
    validation_split=0.2,
    verbose=1
)

# -----------------------------
# ACCURACY PLOT
# -----------------------------
plt.figure()
plt.plot(history.history['accuracy'], label='Train Accuracy')
plt.plot(history.history['val_accuracy'], label='Validation Accuracy')
plt.xlabel('Epochs')
plt.ylabel('Accuracy')
plt.legend()
plt.title('CNN Accuracy')
plt.show()

# -----------------------------
# LOSS PLOT
# -----------------------------
plt.figure()
plt.plot(history.history['loss'], label='Train Loss')
plt.plot(history.history['val_loss'], label='Validation Loss')
plt.xlabel('Epochs')
plt.ylabel('Loss')
plt.legend()
plt.title('CNN Loss')
plt.show()

# -----------------------------
# CONFUSION MATRIX
# -----------------------------
y_pred = model.predict(X_test)
y_pred_cls = np.argmax(y_pred, axis=1)
y_true = np.argmax(y_test, axis=1)

cm = confusion_matrix(y_true, y_pred_cls)

plt.figure(figsize=(8,6))

sns.heatmap(
    cm,
    annot=True,
    fmt='d',
    cmap='viridis',              # 🔥 your reference color
    xticklabels=le.classes_,
    yticklabels=le.classes_,
    annot_kws={"size": 14},      # 🔥 bigger numbers
    linewidths=0.5,
    linecolor='white'
)

plt.xlabel("Predicted")
plt.ylabel("Actual")
plt.title("Confusion Matrix")
plt.show()

# -----------------------------
# CLASSIFICATION REPORT
# -----------------------------
print("\nClassification Report:\n")
print(classification_report(y_true, y_pred_cls, target_names=le.classes_))