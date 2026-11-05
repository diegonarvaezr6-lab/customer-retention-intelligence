
import pandas as pd

# Load original data
df = pd.read_csv("data/telco_churn.csv")

print("\nCUSTOMER RETENTION - DATA CLEANING")
print("=" * 45)

# Convert TotalCharges to numeric
df["TotalCharges"] = pd.to_numeric(
    df["TotalCharges"], errors="coerce"
)

# Identify missing values
missing = df["TotalCharges"].isna().sum()
print(f"Missing TotalCharges: {missing}")

# Fill missing charges with zero for new customers
new_customers = df["tenure"] == 0
df.loc[new_customers & df["TotalCharges"].isna(), "TotalCharges"] = 0

# Create analytical indicators
df["ChurnFlag"] = df["Churn"].map({"Yes": 1, "No": 0})
df["RetainedFlag"] = 1 - df["ChurnFlag"]

# Verify results
print("\nRemaining missing values:")
print(df.isna().sum()[lambda x: x > 0])

print("\nCustomer churn rate:")
print(f"{df['ChurnFlag'].mean() * 100:.2f}%")

# Save cleaned dataset
df.to_csv("data/telco_churn_clean.csv", index=False)

print("\nClean dataset saved successfully!")
print(f"Total customers: {len(df):,}")


