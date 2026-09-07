# Python code to merge Excel sheets after skipping the first 5 into one CSV

import pandas as pd

# Path to your Excel file
excel_file = "Iris-for-Money_2026.xlsm"

# Load the Excel file
xls = pd.ExcelFile(excel_file)

# Get all sheet names
all_sheets = xls.sheet_names

# Skip the first 5 sheets
sheets_to_merge = all_sheets[5:]

# List to store dataframes
dfs = []

# Read and append the remaining sheets
for sheet in sheets_to_merge:
    df = pd.read_excel(xls, sheet_name=sheet)
    dfs.append(df)

# Concatenate all dataframes into one
merged_df = pd.concat(dfs, ignore_index=True)

# Export merged dataframe to CSV
merged_df.to_csv("money.csv", index=False)

print(f"Merged {len(sheets_to_merge)} sheets into 'money.csv'")
