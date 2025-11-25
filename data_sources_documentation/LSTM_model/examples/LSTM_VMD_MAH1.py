# -*- coding: utf-8 -*-
"""
Created on Fri Jul 11 13:57:54 2025

@author: PC
"""

# BSMH
# LSTM ve VMD

import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
from vmdpy import VMD

# 1. Veri yükle
# data = pd.read_csv('verim.csv')
data=pd.read_table("OrnekVeri2.txt",header=None)
X = data.iloc[:, :-1].values
y = data.iloc[:, -1].values

# 2. VMD fonksiyonu
def apply_vmd_to_rows(X, K=5):  # K: eğeri VMD’de mod sayısını ifade eder, genelde 3–8 arası iyi çalışır
    vmd_features = []
    for row in X:
        u, _, _ = VMD(row, alpha=2000, tau=0, K=K, DC=0, init=1, tol=1e-7)
        vmd_row = np.hstack(u)
        vmd_features.append(vmd_row)
    return np.array(vmd_features)

X_vmd = apply_vmd_to_rows(X, K=5)

# 3. Normalize et
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X_vmd)

# 4. LSTM için reshape
X_scaled = X_scaled.reshape((X_scaled.shape[0], 1, X_scaled.shape[1]))

# 5. Train-test ayır
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

# 6. Model tanımı
model = Sequential()
model.add(LSTM(64, input_shape=(X_train.shape[1], X_train.shape[2])))
model.add(Dense(1))
model.compile(optimizer='adam', loss='mse')

# 7. Eğitim
model.fit(X_train, y_train, epochs=50, batch_size=16, verbose=1)

# 8. Tahminler
y_pred = model.predict(X_test).flatten()

# 9. Performans değerlendirme
from sklearn.metrics import r2_score, mean_absolute_percentage_error

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

print(f"R²: {r2_score(y_test, y_pred):.4f}")
print(f"NSE: {nse(y_test, y_pred):.4f}")
print(f"KGE: {kge(y_test, y_pred):.4f}")
print(f"WI: {wi(y_test, y_pred):.4f}")
print(f"MAPE: {mean_absolute_percentage_error(y_test, y_pred)*100:.2f}%")

# 10. Grafik
import matplotlib.pyplot as plt

plt.figure(figsize=(10, 6))
plt.plot(y_test, label='Gözlenen', color='blue')
plt.plot(y_pred, label='Tahmin', color='red', linestyle='--')
plt.title('LSTM VMD Gözlenen vs Tahmin Edilen Değerler')
plt.xlabel('Örnekler')
plt.ylabel('Değer')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
