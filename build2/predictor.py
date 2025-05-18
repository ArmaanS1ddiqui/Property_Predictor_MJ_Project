import pandas as pd
import pickle

# === Load Model ===
def load_model():
    with open("property_price_model.pkl", "rb") as file:
        model = pickle.load(file)
    return model

# === Define the Prediction Function ===
price_years = [f"Price Year {i}" for i in range(1, 11)]

def predict_property_price(df, model, property_code, years_to_predict):
    # **Find Property Data by Property Code**
    property_data = df[df["Property Code"] == property_code]

    # **Check if Property Exists**
    if property_data.empty:
        return "❌ Property Code not found."

    # **Extract Last 7 Years of Known Prices (Year 1 to 7)**
    past_prices = property_data[price_years[:7]].values.flatten().tolist()
    last_known_price = property_data[price_years[9]].values[0]  # **Year 10 Price**

    # **Predict Year 8 to 10 Using Model**
    predicted_prices = list(model.predict([past_prices[:7]])[0])

    # **Predict Beyond Year 10 if More Years are Requested**
    for _ in range(years_to_predict - 3):
        # **Use Last 7 Prices (Past + Predicted) as Input for Next Prediction**
        last_seven = past_prices[-7:] + predicted_prices
        input_for_pred = last_seven[-7:]
        next_pred = model.predict([input_for_pred])[0][-1]  # **Predict Only the Last Year**
        predicted_prices.append(next_pred)

    # **Combine Known and Predicted Prices**
    all_prices = [last_known_price] + predicted_prices  # **Include Year 10 Price**

    # **Calculate Percentage Changes for Each Predicted Year**
    # (This part was missing in the previous version)
    percentage_changes = [
        ((all_prices[i] - all_prices[i - 1]) / all_prices[i - 1]) * 100 for i in range(1, len(all_prices))
    ]

    # **Generate Output with Price and Percentage Changes**
    output_text = f"📊 Predicted Prices for Property {property_code}:\n"
    for i, (price, percent_change) in enumerate(zip(predicted_prices, percentage_changes), start=11):
        # **Add Percentage Change for Each Year in the Output**
        output_text += f"Year {i}: {price:.2f} lakhs ({percent_change:+.2f}% change)\n"

    # **Calculate Total Increase from Year 10 to the Final Predicted Year**
    total_increase = all_prices[-1] - last_known_price
    output_text += f"\n🔹 Total Increase in Price (Year 10 → Year {10 + years_to_predict}): {total_increase:.2f} lakhs\n"

    return output_text
