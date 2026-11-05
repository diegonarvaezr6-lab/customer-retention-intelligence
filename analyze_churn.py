import pandas as pd

df = pd.read_csv("data/telco_churn_clean.csv")

print("\nCUSTOMER RETENTION - BUSINESS ANALYSIS")
print("=" * 50)

def analyze_group(column):
    result = (
        df.groupby(column)
        .agg(
            Customers=("customerID", "count"),
            Churned=("ChurnFlag", "sum"),
            ChurnRate=("ChurnFlag", "mean"),
            AvgMonthlyCharges=("MonthlyCharges", "mean")
        )
        .reset_index()
    )

    result["ChurnRate"] = (result["ChurnRate"] * 100).round(2)
    result["AvgMonthlyCharges"] = result["AvgMonthlyCharges"].round(2)

    return result.sort_values("ChurnRate", ascending=False)

for column in ["Contract", "InternetService", "PaymentMethod"]:
    print(f"\nCHURN ANALYSIS BY {column.upper()}")
    print(analyze_group(column).to_string(index=False))

print("\nANALYSIS COMPLETED")
