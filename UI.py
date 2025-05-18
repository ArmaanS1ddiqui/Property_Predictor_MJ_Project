import PySimpleGUI as sg
import pandas as pd
import pickle
import mysql.connector

# === Step 1: Fetch Data from SQL ===
def fetch_data_from_sql():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="armaan17",
        database="major_project"
    )
    query = "SELECT * FROM properties"
    df_sql = pd.read_sql(query, conn)
    conn.close()
    df_sql.to_csv("property_data_with_codes.csv", index=False)
    return df_sql

df = fetch_data_from_sql()

# === Step 2: Load Model ===
with open("property_price_model.pkl", "rb") as file:
    model = pickle.load(file)

# Extract available locations for dropdown
locations = df['Location'].unique().tolist()

# === Define the Prediction Function ===
price_years = [f"Price Year {i}" for i in range(1, 11)]

def predict_property_price(property_code, years_to_predict):
    property_data = df[df["Property Code"] == property_code]

    if property_data.empty:
        return "❌ Property Code not found."

    past_prices = property_data[price_years[:7]].values.flatten().tolist()
    last_known_price = property_data[price_years[9]].values[0]
    predicted_prices = list(model.predict([past_prices[:7]])[0])

    # Predict beyond Year 10 if needed
    for _ in range(years_to_predict - 3):
        last_seven = past_prices[-7:] + predicted_prices
        next_pred = model.predict([last_seven[-7:]])[0][-1]
        predicted_prices.append(next_pred)

    all_prices = [last_known_price] + predicted_prices
    output_text = f"📊 Predicted Prices for {property_code}:\n"
    for i, price in enumerate(predicted_prices, start=11):
        output_text += f"Year {i}: {price:.2f} lakhs\n"
    total_increase = all_prices[-1] - last_known_price
    output_text += f"\n🔹 Total Increase in Price (Year 10 → Year {10 + years_to_predict}): {total_increase:.2f} lakhs\n"
    return output_text

# === UI Layout ===
layout = [
    [sg.Text("🏠 Property Price Predictor", font=("Helvetica", 20), text_color='blue', justification='center', size=(60, 1))],
    [sg.Text("Select Property Location:", font=("Helvetica", 12))],
    [sg.Combo(locations, key="-LOCATION-", size=(40, 1))],
    [sg.Text("Enter Number of Years to Predict:", font=("Helvetica", 12))],
    [sg.Input(key="-YEARS-", size=(10, 1))],
    [sg.Button("Predict", size=(15, 1)), sg.Button("Exit", size=(15, 1))],
    [sg.Multiline(key="-OUTPUT-", size=(60, 15), font=("Courier", 10))]
]

# === Create the Window ===
window = sg.Window("Property Price Predictor", layout)

# === Event Loop ===
while True:
    event, values = window.read()
    if event == sg.WINDOW_CLOSED or event == "Exit":
        break
    if event == "Predict":
        location = values["-LOCATION-"]
        try:
            years = int(values["-YEARS-"])
            # Find property code for the selected location
            property_code = df.loc[df["Location"] == location, "Property Code"].values[0]
            output = predict_property_price(property_code, years)
            window["-OUTPUT-"].update(output)
        except ValueError:
            window["-OUTPUT-"].update("⚠️ Please enter a valid number of years.")
        except IndexError:
            window["-OUTPUT-"].update("❌ No property code found for the selected location.")

window.close()
