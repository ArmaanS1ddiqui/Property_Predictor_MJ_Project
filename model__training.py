import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score

# Load the data
file_path = 'property_data_cleaned.csv'
data = pd.read_csv(file_path)

# Prepare the data
# Features: Prices and reasons from 2015 to 2019
# Target: Prices from 2020 to 2024

# Extract relevant columns
features = data[['Price Year 1', 'Price Year 2', 'Price Year 3', 'Price Year 4', 'Price Year 5']]

# Convert reasons to numerical values using one-hot encoding
reason_columns = ['Price Year 1 Reason', 'Price Year 2 Reason', 'Price Year 3 Reason', 'Price Year 4 Reason', 'Price Year 5 Reason']
reason_encoded = pd.get_dummies(data[reason_columns], drop_first=True)

# Combine features and encoded reasons
X = pd.concat([features, reason_encoded], axis=1)

# Target variables: Prices from 2020 to 2024
y = data[['Price Year 6', 'Price Year 7', 'Price Year 8', 'Price Year 9', 'Price Year 10']]

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Initialize the model
model = RandomForestRegressor(n_estimators=100, random_state=42)

# Train the model
model.fit(X_train, y_train)

# Predict on the test set
y_pred = model.predict(X_test)

# Calculate accuracy (R^2 score) for each property
accuracy_per_property = [r2_score(y_test.iloc[i], y_pred[i]) for i in range(y_test.shape[0])]

# Check if accuracy is negative or below 80% for any property
if any(acc < 0 for acc in accuracy_per_property):
    print("Negative accuracy detected for some properties. Stopping training.")
elif any(acc < 0.8 for acc in accuracy_per_property):
    print("Accuracy below 80% for some properties. Stopping training.")
else:
    print("All properties have accuracy above 80%.")

# Print accuracy for each property
for i, acc in enumerate(accuracy_per_property):
    print(f"Property {i+1} Accuracy: {acc:.2%}")
