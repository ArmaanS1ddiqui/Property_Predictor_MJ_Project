import pandas as pd
import pickle
import mysql.connector
import random  # Added for random adjustment

# === Load Model ===
def load_model():
    with open("property_price_model.pkl", "rb") as file:
        model = pickle.load(file)
    return model

# === Define the Prediction Function ===
price_years = [f"Price Year {i}" for i in range(1, 11)]

# === Fetch Future Developments from SQL ===
def get_future_factors(property_code):
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="armaan17",
        database="major_project"
    )
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Future_developments WHERE `Property Code` = %s", (property_code,))
    result = cursor.fetchone()
    conn.close()
    return result

def predict_property_price(df, model, property_code, years_to_predict):
    # **Find Property Data by Property Code**
    property_data = df[df["Property Code"] == property_code]

    # **Check if Property Exists**
    if property_data.empty:
        return "❌ Property Code not found."

    # **Extract Last 7 Years of Known Prices (Year 1 to 7)**
    past_prices = property_data[price_years[:7]].values.flatten().tolist()
    last_known_price = property_data[price_years[9]].values[0]  # **Year 10 Price**

    # **Fetch Future Development Factors**
    future_factors = get_future_factors(property_code)

    predicted_prices = []
    factors_used = []
    prev_price = last_known_price

    for year_offset in range(1, years_to_predict + 1):
        last_seven = past_prices[-7:] + predicted_prices
        input_for_pred = last_seven[-7:] if len(last_seven) >= 7 else (last_seven + [prev_price] * (7 - len(last_seven)))
        next_pred = model.predict([input_for_pred])[0][-1]  # **Predict Only the Last Year**

        # **If year within future factor range (1–5), apply factor if available**
        if year_offset <= 5 and future_factors:
            factor = future_factors.get(f"Development Year {year_offset}", "None")
            if factor != "None":
                adjustment = random.uniform(2, 15)  # **Random adjustment between 2 and 15 lakhs**
                next_pred += adjustment
        else:
            factor = "None"

        predicted_prices.append(next_pred)
        percent_change = ((next_pred - prev_price) / prev_price) * 100
        prev_price = next_pred
        factors_used.append((next_pred, percent_change, factor))

    # **Generate Output with Price, Percentage Change, and Factor**
    output_text = f"📊 Predicted Prices for Property {property_code}:\n"
    for i, (price, percent_change, factor) in enumerate(factors_used, start=11):
        output_text += f"Year {i}: {price:.2f} lakhs ({percent_change:+.2f}% change) : {factor}\n"

    # **Calculate Total Increase from Year 10 to the Final Predicted Year**
    total_increase = predicted_prices[-1] - last_known_price
    output_text += f"\n🔹 Total Increase in Price (Year 10 → Year {10 + years_to_predict}): {total_increase:.2f} lakhs\n"

    return output_text