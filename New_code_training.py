"""
Train XGBoost model to predict Price Year 8‑10 and save to pkl
----------------------------------------------------------------
• Requires: pandas, scikit‑learn, xgboost, joblib
• Run:  python train_property_model.py
"""

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.multioutput import MultiOutputRegressor
from sklearn.metrics import mean_absolute_percentage_error, r2_score
from xgboost import XGBRegressor
import joblib
from datetime import datetime

# 1️⃣ LOAD & CLEAN
df = pd.read_csv("property_data_with_codes.csv")
df = df.drop(columns=["Property Code"])      # ID column – not predictive
df = df.dropna()                             # simple missing‑value strategy

# 2️⃣ DEFINE FEATURES / TARGETS
price_cols      = [f"Price Year {i}" for i in range(1, 11)]
input_prices    = price_cols[:7]             # Year 1‑7 → features
target_prices   = price_cols[7:]             # Year 8‑10 → labels

feature_cols = ['BHK', 'Bath', 'Location Class'] + input_prices
X = df[feature_cols]
y = df[target_prices]

# 3️⃣ TRAIN / TEST SPLIT
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.20, random_state=42
)

# 4️⃣ PREPROCESSOR  (one‑hot encode Location Class, leave others)
preprocessor = ColumnTransformer(
    transformers=[
        ('cat', OneHotEncoder(handle_unknown='ignore'), ['Location Class']),
    ],
    remainder='passthrough'
)

# 5️⃣ MODEL  (XGBoost wrapped for multi‑output)
xgb_base = XGBRegressor(
    n_estimators=300,
    learning_rate=0.05,
    max_depth=6,
    subsample=0.8,
    colsample_bytree=0.8,
    objective='reg:squarederror',
    random_state=42,
    n_jobs=-1,
)
model = MultiOutputRegressor(xgb_base)

# 6️⃣ PIPELINE  (preprocessing + model)
pipeline = Pipeline([
    ('prep', preprocessor),
    ('xgb',  model),
])

# 7️⃣ FIT
pipeline.fit(X_train, y_train)

# 8️⃣ QUICK EVALUATION  (optional)
y_pred = pipeline.predict(X_test)
mape   = mean_absolute_percentage_error(y_test, y_pred)
r2     = r2_score(y_test, y_pred)
print(f"MAPE: {mape:.3f}  |  Accuracy: {(1-mape)*100:.2f}%  |  R²: {r2:.3f}")

# 9️⃣ SAVE → PKL
timestamp   = datetime.now().strftime("%Y%m%d_%H%M")
filename    = f"xgboost_property_model_{timestamp}.pkl"
joblib.dump(pipeline, filename)
print(f"✅ Model saved to  '{filename}'")

# 🔟 HOW TO LOAD LATER
# loaded_model = joblib.load(filename)
# preds = loaded_model.predict(new_dataframe_with_same_columns)
