import mysql.connector
from mysql.connector import Error
import pandas as pd

# === CONFIGURATION ===
host = "localhost"
user = "root"
password = "armaan17"  # Change if needed
database_name = "major_project"
table_name = "properties"
csv_file = "property_data_with_codes.csv"

def map_dtype_to_sql(dtype):
    if pd.api.types.is_integer_dtype(dtype):
        return "INT"
    elif pd.api.types.is_float_dtype(dtype):
        return "FLOAT"
    elif pd.api.types.is_object_dtype(dtype):
        return "VARCHAR(255)"
    else:
        return "TEXT"

try:
    # Connect to MySQL
    conn = mysql.connector.connect(host=host, user=user, password=password)

    if conn.is_connected():
        print("✅ Connected to MySQL!")
        cursor = conn.cursor()

        # Create database if it doesn't exist
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {database_name}")
        print(f"📦 Database '{database_name}' is ready.")

        # Switch to the database
        conn.database = database_name

        # Load the CSV file
        df = pd.read_csv(csv_file)

        # Drop table if it exists
        cursor.execute(f"DROP TABLE IF EXISTS {table_name}")

        # Dynamically build CREATE TABLE query from DataFrame
        columns_with_types = ",\n".join([
            f"`{col}` {map_dtype_to_sql(dtype)}"
            for col, dtype in df.dtypes.items()
        ])
        create_table_query = f"CREATE TABLE {table_name} (\n{columns_with_types}\n);"

        cursor.execute(create_table_query)
        print(f"📄 Table '{table_name}' created based on CSV structure.")

        # Insert data
        placeholders = ", ".join(["%s"] * len(df.columns))
        insert_query = f"INSERT INTO {table_name} ({', '.join([f'`{col}`' for col in df.columns])}) VALUES ({placeholders})"

        for _, row in df.iterrows():
            cursor.execute(insert_query, tuple(row))

        conn.commit()
        print("✅ Data uploaded successfully!")

except Error as e:
    print(f"⚠️ Error: {e}")

finally:
    if 'conn' in locals() and conn.is_connected():
        conn.close()
        print("🔒 Connection closed.")
