# -*- coding: utf-8 -*-
"""
Created on Fri Jul 11 13:52:29 2025

@author: PC
"""

# BSMH
# LSTM ve dalgacik eğitimi
import pandas as pd
import numpy as np
import pywt
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense

# 1. Veriyi yükle
# data = pd.read_csv('verim.csv')
# X = data.iloc[:, :-1].values
# y = data.iloc[:, -1].values


data=pd.read_table("OrnekVeri2.txt",header=None)
X = data.iloc[:, :-1].values
y = data.iloc[:, -1].values

# 2. Dalgacık dönüşümü (DWT) uygulama fonksiyonu
def apply_dwt_to_features(X, wavelet='db4', level=3):
    features = []
    for row in X:
        coeffs = pywt.wavedec(row, wavelet, level=level)
        # Tüm katsayıları birleştir
        row_features = np.hstack(coeffs)
        features.append(row_features)
    return np.array(features)

X_dwt = apply_dwt_to_features(X)

# 3. Normalizasyon
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X_dwt)

# 4. Veriyi LSTM formatına uygun hale getir
X_scaled = X_scaled.reshape((X_scaled.shape[0], 1, X_scaled.shape[1]))

# 5. Train-Test ayır
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

# 6. LSTM modeli tanımlama
model = Sequential()
model.add(LSTM(64, input_shape=(X_train.shape[1], X_train.shape[2])))
model.add(Dense(1, activation='linear'))
model.compile(optimizer='adam', loss='mse')

# 7. Modeli eğit
model.fit(X_train, y_train, epochs=50, batch_size=16, verbose=1)

# 8. Başarıyı test et
loss = model.evaluate(X_test, y_test)
print(f"Test Loss: {loss:.4f}")

