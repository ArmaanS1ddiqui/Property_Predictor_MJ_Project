import pickle
import pandas as pd
import numpy as np

# Load the trained model
with open("property_price_model.pkl", "rb") as file:
    model = pickle.load(file)

# Load dataset for reference
df = pd.read_csv("property_data_with_codes.csv")

# Define column names for price years 1 to 10
price_years = [f"Price Year {i}" for i in range(1, 11)]

# User Input: Property Code & Years to Predict
property_code = input("Enter Property Code: ")
years_to_predict = int(input("Enter number of years to predict: "))

# Find Property Data
property_data = df[df["Property Code"] == property_code]

if property_data.empty:
    print("❌ Property Code not found.")
else:
    # Extract last 7 years of prices (Price Year 1 to 7)
    past_prices = property_data[price_years[:7]].values.flatten().tolist()
    last_known_price = property_data[price_years[9]].values[0]  # Price Year 10

    # Predict Price Year 8, 9, 10 (3 years prediction from model)
    predicted_prices = list(model.predict([past_prices[:7]])[0])

    # Predict beyond Year 10 if years_to_predict > 3
    for _ in range(years_to_predict - 3):
        # Create input with last 7 years from past + predicted prices combined
        last_seven = past_prices[-7:] + predicted_prices
        input_for_pred = last_seven[-7:]

        # Predict next year's prices (3 years prediction, take last one)
        next_pred = model.predict([input_for_pred])[0][-1]
        predicted_prices.append(next_pred)

    # Combine last known price (Year 10) with predicted future prices
    all_prices = [last_known_price] + predicted_prices

    # Calculate percentage increases year by year
    percentage_increases = [
        ((all_prices[i] - all_prices[i - 1]) / all_prices[i - 1]) * 100 for i in range(1, len(all_prices))
    ]

    # Display Results
    print(f"\n📊 Predicted Prices for Property {property_code}:")
    for i, (price, percent_inc) in enumerate(zip(predicted_prices, percentage_increases), start=11):
        print(f"Year {i}: {price:.2f} lakhs ({percent_inc:.2f}% increase)")

    # Total Increase from Year 10 to final predicted year
    total_increase = all_prices[-1] - last_known_price
    print(f"\n🔹 Total Increase in Price (Year 10 → Year {10 + years_to_predict}): {total_increase:.2f} lakhs")
