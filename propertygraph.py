import pandas as pd
import matplotlib.pyplot as plt
# Armaans Comment : History Graph
# Load the dataset (replace with your actual file path)
input_file = "property_data_with_codes.csv"
df = pd.read_csv(input_file)

# Display the list of properties with their codes
print("List of Properties:")
for index, row in df.iterrows():
    print(f"Property Code: {row['Property Code']}, Location: {row['Location']}, BHK: {row['BHK']}, Bath: {row['Bath']}, Current Price: {row['Price (in lakhs)']} lakhs")

# Ask the user to enter a Property Code
property_code = input("Enter the Property Code to view its price graph: ")

# Find the property details based on the entered code
property_data = df[df["Property Code"] == property_code]

# Check if the property exists
if property_data.empty:
    print("Property Code not found. Please try again.")
else:
    # Extract property details
    location = property_data["Location"].values[0]
    bhk = property_data["BHK"].values[0]
    bath = property_data["Bath"].values[0]
    current_price = float(property_data["Price Year 10"].values[0])  # Ensure float

    # Extract price history and reasons
    years = list(range(2015, 2025))
    prices = [float(property_data[f"Price Year {i}"].values[0]) for i in range(1, 11)]  # Convert to float
    reasons = [property_data[f"Price Year {i} Reason"].values[0] for i in range(1, 11)]

    # Define colors for each reason
    reason_colors = {
        "NEW METRO": "blue",
        "NEW MALL": "red",
        "NEW SCHOOL": "green",
        "INFLATION": "orange",
        "DEMAND SURGE": "purple",
        "NEW PARK": "brown",
        "ROAD WIDENING": "pink",
        "NONE": "gray"
    }

    # Plot the graph
    plt.figure(figsize=(10, 6))

    for i in range(len(years) - 1):
        plt.plot(
            [years[i], years[i + 1]],
            [prices[i], prices[i + 1]],
            color=reason_colors.get(reasons[i + 1], "gray"),
            marker='o',
            label=reasons[i + 1] if i == 0 else ""
        )

    # Explicitly mark the final data point
    plt.scatter(years[-1], prices[-1], color=reason_colors.get(reasons[-1], "gray"), 
                s=100, edgecolors="black", label="Final Price")

    # Set labels and title
    plt.title(f"Price History for Property: {location} (BHK: {bhk}, Bath: {bath}, Current Price: {current_price} lakhs)")
    plt.xlabel("Year")
    plt.ylabel("Price (in lakhs)")
    plt.xticks(years)

    # ===> FIX: Explicitly define y-axis ticks to match price points
    price_min, price_max = min(prices), max(prices)
    y_tick_step = max(5, (price_max - price_min) // 10)  # Ensure reasonable tick intervals
    plt.yticks(range(int(price_min), int(price_max) + y_tick_step, y_tick_step))

    # ===> FIX: Set y-axis limits based on actual price range, with minimal padding
    plt.ylim(price_min - 2, price_max + 2)  # Small padding to avoid stretching

    plt.grid(True)

    # Add legend
    handles = [plt.Line2D([0], [0], color=color, lw=2) for color in reason_colors.values()]
    plt.legend(handles, reason_colors.keys(), title="Reason for Price Increase", loc="upper left")

    # Show the graph
    plt.show()
