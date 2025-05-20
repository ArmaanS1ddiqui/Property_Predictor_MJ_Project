import pandas as pd
import mysql.connector

# === Load the CSV file ===
csv_file = "future_developments.csv"
df = pd.read_csv(csv_file)

# === Database credentials ===
host = "localhost"
user = "root"
password = "armaan17"
database_name = "major_project"
table_name = "Future_developments"  # <-- Make sure this is what you meant

# === Connect to MySQL ===
conn = mysql.connector.connect(
    host=host,
    user=user,
    password=password,
    database=database_name
)
cursor = conn.cursor()

# === Create the table if it doesn't exist ===
cursor.execute(f"""
    CREATE TABLE IF NOT EXISTS {table_name} (
        `Property Code` VARCHAR(50) PRIMARY KEY,
        `Development Year 1` VARCHAR(50),
        `Development Year 2` VARCHAR(50),
        `Development Year 3` VARCHAR(50),
        `Development Year 4` VARCHAR(50),
        `Development Year 5` VARCHAR(50)
    )
""")

# === Insert data into the table ===
for _, row in df.iterrows():
    cursor.execute(f"""
        INSERT INTO {table_name} 
        (`Property Code`, `Development Year 1`, `Development Year 2`, `Development Year 3`, `Development Year 4`, `Development Year 5`)
        VALUES (%s, %s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE
            `Development Year 1`=VALUES(`Development Year 1`),
            `Development Year 2`=VALUES(`Development Year 2`),
            `Development Year 3`=VALUES(`Development Year 3`),
            `Development Year 4`=VALUES(`Development Year 4`),
            `Development Year 5`=VALUES(`Development Year 5`)
    """, tuple(row))

# === Commit and close ===
conn.commit()
cursor.close()
conn.close()

print("✅ Future_developments data uploaded to MySQL successfully.")
