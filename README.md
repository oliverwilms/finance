# finance

Perfect choice ✅ — PostgreSQL is rock-solid for financial data analysis, and running it locally will give you both performance and control.
Here’s your step-by-step guide to set up PostgreSQL locally and connect it to Streamlit:

1. Install PostgreSQL Locally

Go to postgresql.org/download.
Choose your OS (Windows, macOS, Linux) and download the installer.
During installation:

Set a password for the postgres superuser (remember it).
Install pgAdmin (optional but useful for managing your database visually).




2. Create Your Database
You can do this via pgAdmin or the terminal:
Bashpsql -U postgres
CREATE DATABASE finance;
\q


3. Create a Table for Financial Data
Example table:
SqlCREATE TABLE transactions (
    id SERIAL PRIMARY KEY,
    date DATE NOT NULL,
    description TEXT,
    category TEXT,
    amount NUMERIC(12, 2)
);


4. Insert Sample Data
SqlINSERT INTO transactions (date, description, category, amount)
VALUES
('2026-08-01', 'Stock Purchase', 'Investment', -1500.00),
('2026-08-03', 'Dividend', 'Income', 200.00),
('2026-08-05', 'Office Supplies', 'Expense', -75.50);


5. Connect PostgreSQL to Streamlit
Install dependencies:
Bashpip install psycopg2 pandas streamlit

Example app.py:
Pythonimport streamlit as st
import pandas as pd
import psycopg2

# Connect to PostgreSQL
conn = psycopg2.connect(
    dbname="finance",
    user="postgres",
    password="yourpassword",
    host="localhost",
    port="5432"
)

# Load data
df = pd.read_sql("SELECT * FROM transactions", conn)

# Streamlit UI
st.title("📊 Financial Data Dashboard")
st.dataframe(df)

# Summary
st.write("Total Balance:", df["amount"].sum())

Run your app:
Bashstreamlit run app.py


💡 Tip: For better security, store your DB credentials in a .env file and load them with python-dotenv instead of hardcoding.

If you want, I can extend this setup to include interactive charts and filters in Streamlit so you can visualize your financial data dynamically.
Do you want me to prepare that enhanced dashboard version?

Awesome! 🎯 Let’s upgrade your local PostgreSQL + Streamlit setup into a fully interactive financial dashboard with charts, filters, and summaries.

1. Install Extra Libraries
We’ll use Plotly for charts and python-dotenv for secure credentials.
Bashpip install plotly python-dotenv


2. Store Your DB Credentials Securely
Create a .env file in your project folder:
DB_NAME=finance
DB_USER=postgres
DB_PASSWORD=yourpassword
DB_HOST=localhost
DB_PORT=5432


3. Enhanced Streamlit App (app.py)
Pythonimport streamlit as st
import pandas as pd
import psycopg2
import plotly.express as px
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Connect to PostgreSQL
conn = psycopg2.connect(
    dbname=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    host=os.getenv("DB_HOST"),
    port=os.getenv("DB_PORT")
)

# Load data
df = pd.read_sql("SELECT * FROM transactions ORDER BY date", conn)

# Sidebar filters
st.sidebar.header("🔍 Filters")
category_filter = st.sidebar.multiselect(
    "Select Category",
    options=df["category"].unique(),
    default=df["category"].unique()
)

date_range = st.sidebar.date_input(
    "Select Date Range",
    [df["date"].min(), df["date"].max()]
)

# Apply filters
filtered_df = df[
    (df["category"].isin(category_filter)) &
    (df["date"] >= pd.to_datetime(date_range[0])) &
    (df["date"] <= pd.to_datetime(date_range[1]))
]

# Dashboard title
st.title("📊 Financial Data Dashboard")

# Summary metrics
total_balance = filtered_df["amount"].sum()
total_income = filtered_df[filtered_df["amount"] > 0]["amount"].sum()
total_expense = filtered_df[filtered_df["amount"] < 0]["amount"].sum()

col1, col2, col3 = st.columns(3)
col1.metric("💰 Total Balance", f"${total_balance:,.2f}")
col2.metric("📈 Total Income", f"${total_income:,.2f}")
col3.metric("📉 Total Expenses", f"${total_expense:,.2f}")

# Data table
st.subheader("📄 Transactions")
st.dataframe(filtered_df)

# Charts
st.subheader("📅 Amount Over Time")
fig_time = px.line(filtered_df, x="date", y="amount", color="category", markers=True)
st.plotly_chart(fig_time, use_container_width=True)

st.subheader("📊 Category Breakdown")
fig_pie = px.pie(filtered_df, names="category", values="amount", hole=0.4)
st.plotly_chart(fig_pie, use_container_width=True)


4. Run the Dashboard
Bashstreamlit run app.py

You’ll now have:

Sidebar filters for category and date range
Summary metrics for balance, income, and expenses
Interactive line chart for trends over time
Pie chart for category breakdown
Live data table from PostgreSQL


💡 If you want, I can extend this further so you can add new transactions directly from the Streamlit app and have them saved instantly to PostgreSQL — making it a mini financial management system.
Do you want me to add that transaction input feature next?


Perfect! 🚀
Let’s turn your PostgreSQL + Streamlit dashboard into a mini financial management system where you can add new transactions directly from the app and see them update instantly.

1. Updated Streamlit App with Data Entry
Here’s the enhanced app.py:
Pythonimport streamlit as st
import pandas as pd
import psycopg2
import plotly.express as px
from dotenv import load_dotenv
import os
from datetime import date

# Load environment variables
load_dotenv()

# Connect to PostgreSQL
def get_connection():
    return psycopg2.connect(
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT")
    )

# Function to load data
def load_data():
    conn = get_connection()
    df = pd.read_sql("SELECT * FROM transactions ORDER BY date", conn)
    conn.close()
    return df

# Function to insert new transaction
def add_transaction(date, description, category, amount):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO transactions (date, description, category, amount) VALUES (%s, %s, %s, %s)",
        (date, description, category, amount)
    )
    conn.commit()
    cur.close()
    conn.close()

# Sidebar - Add Transaction
st.sidebar.header("➕ Add New Transaction")
with st.sidebar.form("transaction_form"):
    t_date = st.date_input("Date", value=date.today())
    t_description = st.text_input("Description")
    t_category = st.text_input("Category")
    t_amount = st.number_input("Amount", step=0.01, format="%.2f")
    submitted = st.form_submit_button("Add Transaction")
    if submitted:
        if t_description and t_category and t_amount != 0:
            add_transaction(t_date, t_description, t_category, t_amount)
            st.sidebar.success("✅ Transaction added successfully!")
        else:
            st.sidebar.error("⚠ Please fill all fields and enter a non-zero amount.")

# Load and filter data
df = load_data()

st.sidebar.header("🔍 Filters")
category_filter = st.sidebar.multiselect(
    "Select Category",
    options=df["category"].unique(),
    default=df["category"].unique()
)

date_range = st.sidebar.date_input(
    "Select Date Range",
    [df["date"].min(), df["date"].max()]
)

filtered_df = df[
    (df["category"].isin(category_filter)) &
    (df["date"] >= pd.to_datetime(date_range[0])) &
    (df["date"] <= pd.to_datetime(date_range[1]))
]

# Dashboard
st.title("📊 Financial Data Dashboard")

# Summary metrics
total_balance = filtered_df["amount"].sum()
total_income = filtered_df[filtered_df["amount"] > 0]["amount"].sum()
total_expense = filtered_df[filtered_df["amount"] < 0]["amount"].sum()

col1, col2, col3 = st.columns(3)
col1.metric("💰 Total Balance", f"${total_balance:,.2f}")
col2.metric("📈 Total Income", f"${total_income:,.2f}")
col3.metric("📉 Total Expenses", f"${total_expense:,.2f}")

# Data table
st.subheader("📄 Transactions")
st.dataframe(filtered_df)

# Charts
st.subheader("📅 Amount Over Time")
fig_time = px.line(filtered_df, x="date", y="amount", color="category", markers=True)
st.plotly_chart(fig_time, use_container_width=True)

st.subheader("📊 Category Breakdown")
fig_pie = px.pie(filtered_df, names="category", values="amount", hole=0.4)
st.plotly_chart(fig_pie, use_container_width=True)


2. How It Works

Sidebar Form → Lets you enter a date, description, category, and amount.
Instant Save → Data is inserted into PostgreSQL immediately.
Auto Refresh → The dashboard reloads with the new transaction.


3. Run the App
Bashstreamlit run app.py

You now have:
✅ Live database connection
✅ Interactive filters & charts
✅ Ability to add transactions without leaving the app

If you want, I can extend this even further so you can edit or delete transactions directly from the dashboard — making it a full CRUD (Create, Read, Update, Delete) financial tracker.
Do you want me to add that edit/delete



Alright — let’s make your PostgreSQL + Streamlit financial dashboard a full CRUD app so you can Create, Read, Update, and Delete transactions directly from the interface.
This will turn it into a complete local financial management system.

1. Updated app.py with Edit & Delete
Pythonimport streamlit as st
import pandas as pd
import psycopg2
import plotly.express as px
from dotenv import load_dotenv
import os
from datetime import date

# Load environment variables
load_dotenv()

# Database connection
def get_connection():
    return psycopg2.connect(
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT")
    )

# Load data
def load_data():
    conn = get_connection()
    df = pd.read_sql("SELECT * FROM transactions ORDER BY date", conn)
    conn.close()
    return df

# Insert transaction
def add_transaction(date, description, category, amount):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO transactions (date, description, category, amount) VALUES (%s, %s, %s, %s)",
        (date, description, category, amount)
    )
    conn.commit()
    cur.close()
    conn.close()

# Update transaction
def update_transaction(t_id, date, description, category, amount):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "UPDATE transactions SET date=%s, description=%s, category=%s, amount=%s WHERE id=%s",
        (date, description, category, amount, t_id)
    )
    conn.commit()
    cur.close()
    conn.close()

# Delete transaction
def delete_transaction(t_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM transactions WHERE id=%s", (t_id,))
    conn.commit()
    cur.close()
    conn.close()

# Sidebar - Add Transaction
st.sidebar.header("➕ Add New Transaction")
with st.sidebar.form("transaction_form"):
    t_date = st.date_input("Date", value=date.today())
    t_description = st.text_input("Description")
    t_category = st.text_input("Category")
    t_amount = st.number_input("Amount", step=0.01, format="%.2f")
    submitted = st.form_submit_button("Add Transaction")
    if submitted:
        if t_description and t_category and t_amount != 0:
            add_transaction(t_date, t_description, t_category, t_amount)
            st.sidebar.success("✅ Transaction added successfully!")
        else:
            st.sidebar.error("⚠ Please fill all fields and enter a non-zero amount.")

# Load and filter data
df = load_data()

st.sidebar.header("🔍 Filters")
category_filter = st.sidebar.multiselect(
    "Select Category",
    options=df["category"].unique(),
    default=df["category"].unique()
)

date_range = st.sidebar.date_input(
    "Select Date Range",
    [df["date"].min(), df["date"].max()]
)

filtered_df = df[
    (df["category"].isin(category_filter)) &
    (df["date"] >= pd.to_datetime(date_range[0])) &
    (df["date"] <= pd.to_datetime(date_range[1]))
]

# Dashboard
st.title("📊 Financial Data Dashboard")

# Summary metrics
total_balance = filtered_df["amount"].sum()
total_income = filtered_df[filtered_df["amount"] > 0]["amount"].sum()
total_expense = filtered_df[filtered_df["amount"] < 0]["amount"].sum()

col1, col2, col3 = st.columns(3)
col1.metric("💰 Total Balance", f"${total_balance:,.2f}")
col2.metric("📈 Total Income", f"${total_income:,.2f}")
col3.metric("📉 Total Expenses", f"${total_expense:,.2f}")

# Data table
st.subheader("📄 Transactions")
st.dataframe(filtered_df)

# Edit/Delete section
st.subheader("✏️ Edit or 🗑 Delete Transactions")
transaction_ids = filtered_df["id"].tolist()
selected_id = st.selectbox("Select Transaction ID", transaction_ids)

if selected_id:
    selected_row = df[df["id"] == selected_id].iloc[0]
    with st.form("edit_form"):
        e_date = st.date_input("Date", value=selected_row["date"])
        e_description = st.text_input("Description", value=selected_row["description"])
        e_category = st.text_input("Category", value=selected_row["category"])
        e_amount
