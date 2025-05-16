import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_percentage_error, r2_score
from xgboost import XGBRegressor

# Load dataset
df = pd.read_csv("property_data_with_codes.csv")

# Drop unnecessary columns
df.drop(columns=["Property Code"], inplace=True)

# Handle missing values
df.dropna(inplace=True)

# Define feature and target column names
price_years = [f"Price Year {i}" for i in range(1, 11)]
input_features = price_years[:7]  # Price Year 1 - 7
target_features = price_years[7:]  # Price Year 8 - 10

# Define features (X) and target (Y)
X = df[input_features]
Y = df[target_features]

# Split dataset (80% train, 20% test)
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, random_state=42)

# Define models
models = {
    "Linear Regression": LinearRegression(),
    "Random Forest": RandomForestRegressor(n_estimators=200, random_state=42),
    "XGBoost": XGBRegressor(n_estimators=200, learning_rate=0.1, max_depth=6, random_state=42)
}

# Store results
results = {}

# Train and evaluate models
for name, model in models.items():
    model.fit(X_train, Y_train)
    Y_pred = model.predict(X_test)

    # Compute accuracy metrics
    mape = mean_absolute_percentage_error(Y_test, Y_pred)
    r2 = r2_score(Y_test, Y_pred)
    accuracy = (1 - mape) * 100  # Convert to percentage

    # Store results
    results[name] = accuracy

    # Print results
    print(f"{name}: {accuracy:.2f}% Accuracy (R² Score: {r2:.2f})")

# Find best model
best_model = max(results, key=results.get)
print(f"\n✅ Best Model: {best_model} with {results[best_model]:.2f}% Accuracy")

# Predict with best model
best_pred = models[best_model].predict(X_test)

# === 📊 1. Scatter Plot: Actual vs Predicted ===
plt.figure(figsize=(10, 5))
plt.scatter(Y_test.values.flatten(), best_pred.flatten(), color='red', alpha=0.6, label="Predicted Prices")
plt.plot(Y_test.values.flatten(), Y_test.values.flatten(), color='blue', label="Actual Prices")
plt.xlabel("Actual Prices")
plt.ylabel("Predicted Prices")
plt.title(f"Scatter Plot: Actual vs Predicted Prices ({best_model})")
plt.legend()
plt.tight_layout()
plt.show()

# === 📈 2. Line Plot ===
plt.figure(figsize=(12, 6))
plt.plot(Y_test.values.flatten(), label="Actual Prices", color='blue', linewidth=2)
plt.plot(best_pred.flatten(), label="Predicted Prices", color='red', linestyle='--', linewidth=2)
plt.title(f"Line Plot: Actual vs Predicted Prices ({best_model})")
plt.xlabel("Sample Index")
plt.ylabel("Price")
plt.legend()
plt.tight_layout()
plt.show()

# === 🔍 3. Residual Plot ===
residuals = Y_test.values.flatten() - best_pred.flatten()
plt.figure(figsize=(10, 5))
sns.scatterplot(x=best_pred.flatten(), y=residuals, alpha=0.6, color='purple')
plt.axhline(0, color='black', linestyle='--')
plt.title(f"Residual Plot ({best_model})")
plt.xlabel("Predicted Prices")
plt.ylabel("Residuals (Actual - Predicted)")
plt.tight_layout()
plt.show()

# === 📊 4. KDE Plot ===
plt.figure(figsize=(10, 5))
sns.kdeplot(Y_test.values.flatten(), label="Actual Prices", fill=True, color='blue')
sns.kdeplot(best_pred.flatten(), label="Predicted Prices", fill=True, color='red')
plt.title(f"KDE Plot: Price Distribution ({best_model})")
plt.xlabel("Price")
plt.legend()
plt.tight_layout()
plt.show()
