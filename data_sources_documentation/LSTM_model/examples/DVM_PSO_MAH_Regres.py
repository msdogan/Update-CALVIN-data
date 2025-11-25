# -*- coding: utf-8 -*-
"""
Created on Fri Jul 11 14:51:38 2025

@author: PC
"""

# BSMH
 # DVM_PSO regression
# IT WORKSS!!!!!!!!!##########
 
import numpy as np
import pandas as pd
from sklearn.svm import SVR
from sklearn.model_selection import cross_val_predict, train_test_split
from sklearn.preprocessing import StandardScaler
from pyswarm import pso  # pip install pyswarm
import matplotlib.pyplot as plt

# 1. Veri yükleme
# data = pd.read_csv('veriniz.csv')
data=pd.read_table("OrnekVeri2.txt",header=None)

X = data.iloc[:, :-1].values
y = data.iloc[:, -1].values
X = StandardScaler().fit_transform(X)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 2. Hedef fonksiyon
def svr_score(params):
    C, gamma = params
    model = SVR(C=C, gamma=gamma)
    preds = cross_val_predict(model, X_train, y_train, cv=3)
    return np.mean((preds - y_train)**2)  # MSE

# 3. PSO
lb, ub = [0.1, 0.0001], [100, 10]
best_params, _ = pso(svr_score, lb, ub, swarmsize=30, maxiter=20)

# 4. Eğitilmiş model
model_pso = SVR(C=best_params[0], gamma=best_params[1])
model_pso.fit(X_train, y_train)
y_pred = model_pso.predict(X_test)

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

# 5. Sonuçlar
print(f"R²: {r2_score(y_test, y_pred):.4f}")
print(f"NSE: {nse(y_test, y_pred):.4f}")
print(f"KGE: {kge(y_test, y_pred):.4f}")
print(f"WI: {wi(y_test, y_pred):.4f}")
print(f"MAPE: {mean_absolute_percentage_error(y_test, y_pred)*100:.2f}%")

plt.figure(figsize=(10, 6))
plt.plot(y_test, label='Gözlenen', color='blue')
plt.plot(y_pred, label='Tahmin', color='red', linestyle='--')
plt.title('Gözlenen vs Tahmin Edilen Değerler (PSO + SVR)')
plt.xlabel('Örnekler')
plt.ylabel('Değer')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

