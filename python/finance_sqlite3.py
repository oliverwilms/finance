import sqlite3
import pandas as pd
import os
import matplotlib.pyplot as plt

# ==============================
# CONFIGURATION
# ==============================
CSV_FILE = "transactions.csv"  # CSV file with: date, description, amount
DB_FILE = "finance.db"

# ==============================
# STEP 1: CREATE DATABASE & TABLE
# ==============================
def create_database():
    conn = sqlite3.connect(DB_FILE)
    conn.execute("""
    CREATE TABLE IF NOT EXISTS transactions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT NOT NULL,
        description TEXT,
        amount REAL NOT NULL
    )
    """)
    conn.commit()
    conn.close()

# ==============================
# STEP 2: IMPORT CSV INTO DATABASE
# ==============================
def import_csv_to_db():
    if not os.path.exists(CSV_FILE):
        print(f"CSV file '{CSV_FILE}' not found. Please create it first.")
        return

    df = pd.read_csv(CSV_FILE)

    # Validate CSV columns
    required_cols = {"date", "description", "amount"}
    if not required_cols.issubset(df.columns):
        print(f"CSV must contain columns: {required_cols}")
        return

    conn = sqlite3.connect(DB_FILE)
    df.to_sql("transactions", conn, if_exists="append", index=False)
    conn.close()
    print(f"Imported {len(df)} records from {CSV_FILE} into {DB_FILE}")

# ==============================
# STEP 3: RUN ANALYSIS
# ==============================
def run_analysis():
    conn = sqlite3.connect(DB_FILE)
    df = pd.read_sql_query("SELECT * FROM transactions", conn)

    if df.empty:
        print("No transactions found in database.")
        conn.close()
        return

    # Convert date column to datetime
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df = df.dropna(subset=["date"])  # Remove invalid dates

    # Calculate totals
    total_income = df[df["amount"] > 0]["amount"].sum()
    total_expense = df[df["amount"] < 0]["amount"].sum()
    net_balance = total_income + total_expense

    # Monthly summary
    monthly_summary = df.groupby(df["date"].dt.to_period("M"))["amount"].sum().reset_index()
    monthly_summary["date"] = monthly_summary["date"].astype(str)

    conn.close()

    # Display results
    print("\n=== Financial Summary ===")
    print(f"Total Income : ${total_income:,.2f}")
    print(f"Total Expense: ${total_expense:,.2f}")
    print(f"Net Balance  : ${net_balance:,.2f}")

    print("\n=== Monthly Summary ===")
    print(monthly_summary.to_string(index=False))

    # ==============================
    # STEP 4: PLOT CHARTS
    # ==============================
    plt.figure(figsize=(8, 5))
    plt.plot(monthly_summary["date"], monthly_summary["amount"], marker="o", label="Net Amount")
    plt.axhline(0, color="black", linewidth=0.8)
    plt.title("Monthly Net Amount")
    plt.xlabel("Month")
    plt.ylabel("Amount ($)")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()

    # Income vs Expense bar chart
    monthly_income = df[df["amount"] > 0].groupby(df["date"].dt.to_period("M"))["amount"].sum().reset_index()
    monthly_expense = df[df["amount"] < 0].groupby(df["date"].dt.to_period("M"))["amount"].sum().reset_index()

    monthly_income["date"] = monthly_income["date"].astype(str)
    monthly_expense["date"] = monthly_expense["date"].astype(str)

    plt.figure(figsize=(8, 5))
    plt.bar(monthly_income["date"], monthly_income["amount"], label="Income", color="green")
    plt.bar(monthly_expense["date"], monthly_expense["amount"], label="Expense", color="red")
    plt.title("Monthly Income vs Expenses")
    plt.xlabel("Month")
    plt.ylabel("Amount ($)")
    plt.legend()
    plt.grid(True, axis="y")
    plt.tight_layout()
    plt.show()

# ==============================
# MAIN EXECUTION
# ==============================
if __name__ == "__main__":
    create_database()
    import_csv_to_db()
    run_analysis()
