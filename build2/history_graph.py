import pandas as pd
import matplotlib.pyplot as plt

def plot_property_history(property_code, df):
    # Find the property details based on the entered code
    property_data = df[df["Property Code"] == property_code]

    # Check if the property exists
    if property_data.empty:
        print("❌ Property Code not found. Please try again.")
        return

    # Extract property details
    location = property_data["Location"].values[0]
    bhk = property_data["BHK"].values[0]
    bath = property_data["Bath"].values[0]
    current_price = float(property_data["Price Year 10"].values[0])

    # Extract price history and reasons
    years = list(range(2015, 2025))
    prices = [float(property_data[f"Price Year {i}"].values[0]) for i in range(1, 11)]
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
    plt.figure(figsize=(12, 8))

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

    # Set y-axis ticks to match price points
    price_min, price_max = min(prices), max(prices)
    y_tick_step = max(5, (price_max - price_min) // 10)
    plt.yticks(range(int(price_min), int(price_max) + y_tick_step, y_tick_step))

    # Set y-axis limits with minimal padding
    plt.ylim(price_min - 2, price_max + 2)

    plt.grid(True)

    # Add legend
    handles = [plt.Line2D([0], [0], color=color, lw=2) for color in reason_colors.values()]
    plt.legend(handles, reason_colors.keys(), title="Reason for Price Increase", loc="upper left")

    # Show the graph
    plt.show()
