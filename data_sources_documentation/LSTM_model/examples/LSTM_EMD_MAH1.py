# -*- coding: utf-8 -*-
"""
Created on Fri Jul 11 14:00:53 2025

@author: PC
"""

# BSMH
# LSTM ve EMD

# aşağıdaki paketler kurulmalıdır
# pip install PyEMD
# pip install tensorflow scikit-learn matplotlib


import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from PyEMD import EMD
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
from sklearn.metrics import r2_score, mean_absolute_percentage_error
import matplotlib.pyplot as plt

# 1. Veri yükleme
# data = pd.read_csv('verim.csv')
data=pd.read_table("OrnekVeri2.txt",header=None)

X = data.iloc[:, :-1].values
y = data.iloc[:, -1].values

# 2. EMD uygulama
def apply_emd_to_rows(X):
    emd_features = []
    for row in X:
        imfs = EMD().emd(row)
        # IMF'leri birleştir
        emd_row = np.hstack(imfs[:5])  # İlk 5 IMF alınabilir
        emd_features.append(emd_row)
    return np.array(emd_features)

X_emd = apply_emd_to_rows(X)

# 3. Normalizasyon
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X_emd)

# 4. LSTM formatına uygun hale getirme
X_scaled = X_scaled.reshape((X_scaled.shape[0], 1, X_scaled.shape[1]))

# 5. Train-Test ayır
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

# 6. LSTM modeli
model = Sequential()
model.add(LSTM(64, input_shape=(X_train.shape[1], X_train.shape[2])))
model.add(Dense(1))
model.compile(optimizer='adam', loss='mse')
model.fit(X_train, y_train, epochs=50, batch_size=16, verbose=1)

# 7. Tahmin ve değerlendirme
y_pred = model.predict(X_test).flatten()

def nse(y_true, y_pred):
    return 1 - np.sum((y_pred - y_true)**2) / np.sum((y_true - np.mean(y_true))**2)

def kge(y_true, y_pred):
    r = np.corrcoef(y_true, y_pred)[0, 1]
    alpha = np.std(y_pred) / np.std(y_true)
    beta = np.mean(y_pred) / np.mean(y_true)
    return 1 - np.sqrt((r - 1)**2 + (alpha - 1)**2 + (beta - 1)**2)

def wi(y_true, y_pred):
    numerator = np.sum((y_pred - y_true)**2)
    denominator = np.sum((np.abs(y_pred - np.mean(y_true)) + np.abs(y_true - np.mean(y_true)))**2)
    return 1 - (numerator / denominator)

# 8. Sonuçları yazdır
print(f"R²: {r2_score(y_test, y_pred):.4f}")
print(f"NSE: {nse(y_test, y_pred):.4f}")
print(f"KGE: {kge(y_test, y_pred):.4f}")
print(f"Willmott Index (WI): {wi(y_test, y_pred):.4f}")
print(f"MAPE: {mean_absolute_percentage_error(y_test, y_pred)*100:.2f}%")

# 9. Grafik
plt.figure(figsize=(10, 6))
plt.plot(y_test, label='Gözlenen', color='blue')
plt.plot(y_pred, label='Tahmin', color='red', linestyle='--')
plt.title('Gözlenen vs Tahmin Edilen Değerler (EMD + LSTM)')
plt.xlabel('Örnekler')
plt.ylabel('Değer')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

