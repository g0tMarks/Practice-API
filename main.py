import os
import requests
import json
from dotenv import load_dotenv
from datetime import datetime
import matplotlib.pyplot as plt

#load .env file
load_dotenv()


# Parameters
symbol = "NVDA"
start_date = "2025-10-06"
end_date = "2025-10-10"

# Marketstack API endpoint for historical data
url = "https://api.marketstack.com/v1/eod"

params = {
    "access_key": os.getenv("API_KEY"),
    "symbols": symbol,
    "date_from": start_date,
    "date_to": end_date,
    "limit": 1000  # optional: max results per page
}

# Make the request
response = requests.get(url, params=params)
data = response.json()
pretty_json_string = json.dumps(data, indent=4)
print(pretty_json_string)

# Check if the response contains valid data
if "data" not in data:
    print("Error:", data)  # Print the error message if 'data' key is missing (e.g., invalid key)
    exit()                 # Stop execution if no valid data is returned

# Inside that dictionary, one of the keys is "data", and its value is a list of dictionaries.
# Where each dictionary represents one day’s stock information.
# Marketstack returns data in reverse chronological order (newest first)
# Sort the entries by date so the graph goes from oldest → newest
# The sorted() function returns a new list with the elements sorted in ascending order.
# We use the key argument to tell Python what property to use when sorting.
# A lambda function is an anonymous (unnamed) mini function that performs one operation.
# In this case, for each x (each daily stock record), the function returns the "date" value, such as "2025-03-31T00:00:00+0000".
# The sorted() function then arranges the records in ascending order based on this date string.
# Since Marketstack returns the newest records first (reverse chronological order).
# This sorts the data so that oldest dates appear first — which is the logical order for plotting a timeline on a chart. 
entries = sorted(data["data"], key=lambda x: x["date"])
print(entries)

# Extract the date (YYYY-MM-DD) for each entry
dates = [entry["date"][:10] for entry in entries]  # [:10] trims the time part from the timestamp

# Extract the corresponding closing price for each date
closes = [entry["close"] for entry in entries]

# Create a new figure for the plot with a specified width and height
plt.figure(figsize=(20, 5))

# Plot the closing prices over time
plt.plot(dates, closes, marker='o', color='blue')  # Circles for data points, blue line

# Add a title and axis labels
plt.title(f"{symbol} Closing Prices (Marketstack)")
plt.xlabel("Date")
plt.ylabel("Close Price (USD)")

# Rotate the x-axis labels for readability
plt.xticks(rotation=45)

# Add a grid for easier reading of data values
plt.grid(True)

# Automatically adjust layout so labels and titles fit neatly
plt.tight_layout()

# Display the line chart
plt.show()

# Save the plot as an image file
plt.savefig("stock_chart_marketstack.png")