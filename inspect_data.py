
import pandas as pd

# Load the original customer dataset
df = pd.read_csv("data/telco_churn.csv")

print("\nCUSTOMER RETENTION INTELLIGENCE")
print("=" * 45)

print("\nTotal rows:", len(df))
print("Total columns:", len(df.columns))

print("\nCOLUMN NAMES:")
print(df.columns.tolist())

print("\nFIRST 5 ROWS:")
print(df.head().to_string())

print("\nMISSING VALUES:")
print(df.isnull().sum().to_string())

print("\nDUPLICATE CUSTOMER IDS:")
print(df["customerID"].duplicated().sum())

print("\nCHURN DISTRIBUTION:")
print(df["Churn"].value_counts().to_string())

print("\nDATA INSPECTION COMPLETED")


