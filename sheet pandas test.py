import pandas as pd
import ssl

# Disable SSL verification (not ideal for sensitive data)
ssl._create_default_https_context = ssl._create_unverified_context

# https://docs.google.com/spreadsheets/d/1XNZp7lGWGmwjJKEVIpjE-aCIXwpAJNSSihOwhrg4b_o/edit?usp=sharing

# Google Sheet ID and Sheet Name
sheet_id = "1XNZp7lGWGmwjJKEVIpjE-aCIXwpAJNSSihOwhrg4b_o"
sheet_name = "Sheet1"

# URL for CSV export
url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}"

# Load data
df = pd.read_csv(url)

# Get the last cell of the first column
last_cell = df.iloc[-1, 0]

print(f"Last cell in the first column: {last_cell}")
