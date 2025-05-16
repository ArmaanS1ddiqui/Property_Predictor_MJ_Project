import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split, RandomizedSearchCV
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_percentage_error, r2_score
from xgboost import XGBRegressor
from scipy.stats import randint as sp_randint, uniform

# 1. Load & clean
df = pd.read_csv("property_data_with_codes.csv")
df.drop(columns=["Property Code"], inplace=True)
df.dropna(inplace=True)

# 2. Features & target
price_years     = [f"Price Year {i}" for i in range(1, 11)]
X = df[price_years[:7]]
Y = df[price_years[7:]]

# 3. Train/Test split
X_train, X_test, Y_train, Y_test = train_test_split(
    X, Y, test_size=0.2, random_state=42
)

# 4. Tune & train RF
rf = RandomForestRegressor(random_state=42)
rf_params = {
    "n_estimators":    sp_randint(100, 300),
    "max_depth":       sp_randint(5, 20),
    "min_samples_split": [2,5,10],
    "min_samples_leaf":  [1,2,4],
    "bootstrap":         [True, False]
}
rf_search = RandomizedSearchCV(rf, rf_params,
    n_iter=20, cv=3, n_jobs=-1, random_state=42, verbose=0
)
rf_search.fit(X_train, Y_train)
best_rf = rf_search.best_estimator_

# 5. Tune & train XGB
xgb = XGBRegressor(objective="reg:squarederror", random_state=42)
xgb_params = {
    "n_estimators":    sp_randint(100, 300),
    "max_depth":       sp_randint(3, 10),
    "learning_rate":   uniform(0.01, 0.3),
    "subsample":       uniform(0.6, 0.4),
    "colsample_bytree":uniform(0.6, 0.4)
}
xgb_search = RandomizedSearchCV(xgb, xgb_params,
    n_iter=20, cv=3, n_jobs=-1, random_state=42, verbose=0
)
xgb_search.fit(X_train, Y_train)
best_xgb = xgb_search.best_estimator_

# 6. Ensemble predictions (average)
pred_rf  = best_rf.predict(X_test)
pred_xgb = best_xgb.predict(X_test)
pred_ensemble = (pred_rf + pred_xgb) / 2.0

# 7. Evaluate ensemble
mape = mean_absolute_percentage_error(Y_test, pred_ensemble)
r2   = r2_score(Y_test, pred_ensemble)
accuracy = (1 - mape) * 100
print(f"Ensemble Model Accuracy: {accuracy:.2f}% (R²: {r2:.2f})")

# Flatten arrays for plotting
actual = Y_test.values.flatten()
preds  = pred_ensemble.flatten()
resids = actual - preds
idx    = np.arange(len(actual))

# ==== 1) Scatter Actual vs Predicted ====
plt.figure(figsize=(6,6))
plt.scatter(actual, preds, alpha=0.6)
plt.plot(actual, actual, '--', color='gray')
plt.xlabel("Actual Prices")
plt.ylabel("Ensembled Predictions")
plt.title("1) Actual vs Predicted (Ensemble)")
plt.tight_layout()
plt.show()

# ==== 2) Residuals Histogram ====
plt.figure(figsize=(6,4))
plt.hist(resids, bins=30, edgecolor='black', alpha=0.7)
plt.xlabel("Residual (Actual – Predicted)")
plt.ylabel("Frequency")
plt.title("2) Residuals Distribution")
plt.tight_layout()
plt.show()

# ==== 3) Predicted & Actual over Sample Index ====
plt.figure(figsize=(8,4))
plt.plot(idx, actual, label="Actual", linewidth=2)
plt.plot(idx, preds,  label="Ensemble Pred", linewidth=2, linestyle='--')
plt.xlabel("Sample Index")
plt.ylabel("Price")
plt.title("3) Actual vs Ensemble Prediction Over Samples")
plt.legend()
plt.tight_layout()
plt.show()
