import pandas as pd
import mysql.connector
from predictor import load_model, predict_property_price
from history_graph import plot_property_history

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
    return df_sql

def show_menu():
    print("\n--- Menu ---")
    print("1. Show Historical Data")
    print("2. Predict Property Price")
    print("3. Exit")

def main():
    print("Fetching data from database...")
    df = fetch_data_from_sql()
    model = load_model()
    print("Data loaded successfully.\n")

    print("Available Properties:")
    for idx, row in df.iterrows():
        print(f"{row['Property Code']} - {row['Location']}")

    while True:
        show_menu()
        choice = input("Enter your choice: ").strip()

        if choice == '1':
            prop_code = input("Enter Property Code to view history: ").strip()
            plot_property_history(prop_code, df)
        elif choice == '2':
            prop_code = input("Enter Property Code: ").strip()
            try:
                years = int(input("Enter number of years to predict: "))
                result = predict_property_price(df, model, prop_code, years)
                print("\n" + result)
            except ValueError:
                print("⚠️ Please enter a valid number for years.")
        elif choice == '3':
            print("Exiting... Goodbye!")
            break
        else:
            print("Invalid choice, please select again.")

if __name__ == "__main__":
    main()
