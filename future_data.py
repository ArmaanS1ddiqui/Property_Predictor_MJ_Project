import pandas as pd
import random

# === Step 1: Load the property codes from the existing dataset ===
input_file = "property_data_with_codes.csv"
df = pd.read_csv(input_file)

# Get unique property codes
property_codes = df["Property Code"].unique()

# === Step 2: Define possible future development factors ===
factors = [
    "NEW METRO", "NEW MALL", "NEW SCHOOL",
    "INFLATION", "DEMAND SURGE", "NEW PARK", "ROAD WIDENING", "NONE"
]

# === Step 3: Create sparse future development data ===
future_data = []

for code in property_codes:
    row = {"Property Code": code}
    for year in range(1, 6):  # Development Year 1 to 5
        # 80% chance of 'NONE', 20% chance of a real development
        row[f"Development Year {year}"] = (
            random.choice(factors[:-1]) if random.random() < 0.2 else "NONE"
        )
    future_data.append(row)

# === Step 4: Save to CSV ===
output_df = pd.DataFrame(future_data)
output_df.to_csv("future_developments.csv", index=False)

print("✅ future_developments.csv has been created successfully.")
