import pandas as pd
import sqlite3

# Load cleaned customer data
df = pd.read_csv("data/telco_churn_clean.csv")

# Connect to SQLite database
connection = sqlite3.connect("data/customer_retention.db")

# Create SQL table
df.to_sql(
    "customers",
    connection,
    if_exists="replace",
    index=False
)

# Verify imported data
result = pd.read_sql_query(
    """
    SELECT
        COUNT(*) AS total_customers,
        SUM(ChurnFlag) AS churned_customers,
        ROUND(AVG(ChurnFlag) * 100, 2) AS churn_rate
    FROM customers
    """,
    connection
)

print("\nCUSTOMER RETENTION - SQL DATABASE")
print("=" * 45)
print(result.to_string(index=False))

connection.close()

print("\nDatabase created successfully!")
print("Location: data/customer_retention.db")
