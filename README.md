# Customer Retention Intelligence
**Live Interactive Dashboard:** https://customer-retention-intelligence-diego.streamlit.app/

## Project Overview

An end-to-end customer retention analytics project using Python, SQL, SQLite, Streamlit, and Plotly.

This project analyzes the IBM Telco Customer Churn sample dataset to identify customer segments associated with higher churn rates and explore opportunities for improving retention.

## Business Questions

- What percentage of customers churn?
- Which contract types have the highest churn rates?
- How does internet service relate to churn?
- Which payment methods are associated with higher churn?
- How does customer tenure relate to retention?

## Technologies

- Python
- Pandas and NumPy
- SQLite and SQL
- Streamlit
- Plotly
- Git and GitHub

## Key Findings

| Metric | Result |
|---|---|
| Total Customers | 7,043 |
| Churned Customers | 1,869 |
| Overall Churn Rate | 26.54% |
| Month-to-Month Contract Churn | 42.71% |
| Fiber Optic Churn | 41.89% |
| Electronic Check Churn | 45.29% |

## Business Recommendations

1. Prioritize retention outreach for month-to-month customers.
2. Investigate customer experience among fiber optic subscribers.
3. Review payment friction and customer behavior associated with electronic checks.
4. Develop targeted retention campaigns for newer customers.
5. Track churn rates across customer segments over time.

These findings describe associations in a sample dataset and do not establish causation.

## Project Structure

- `data/` - Original and cleaned datasets
- `clean_data.py` - Data cleaning
- `analyze_churn.py` - Exploratory analysis
- `create_database.py` - SQLite database creation
- `sql/business_analysis.sql` - Business SQL queries
- `dashboard.py` - Interactive Streamlit dashboard
- `requirements.txt` - Python dependencies

## Run Locally

Install dependencies:

    pip install -r requirements.txt

Launch the dashboard:

    streamlit run dashboard.py

## Dataset

IBM Telco Customer Churn sample dataset.

This is a public demonstration dataset, not actual operational customer data.

## Author

Diego Narvaez

Information Science - Data Science & Analytics
University of South Florida

LinkedIn:
https://www.linkedin.com/in/diego-narvaez-0918b4358/
