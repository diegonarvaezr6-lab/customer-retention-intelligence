-- CUSTOMER RETENTION INTELLIGENCE
-- Business Analysis with SQLite

-- 1. Executive KPIs
SELECT
    COUNT(*) AS total_customers,
    SUM(ChurnFlag) AS churned_customers,
    ROUND(AVG(ChurnFlag) * 100, 2) AS churn_rate_pct,
    ROUND(SUM(CASE
        WHEN ChurnFlag = 1 THEN MonthlyCharges
        ELSE 0
    END), 2) AS churned_monthly_charges
FROM customers;

-- 2. Churn by contract type
SELECT
    Contract,
    COUNT(*) AS customers,
    SUM(ChurnFlag) AS churned,
    ROUND(AVG(ChurnFlag) * 100, 2) AS churn_rate_pct
FROM customers
GROUP BY Contract
ORDER BY churn_rate_pct DESC;

-- 3. Churn by internet service
SELECT
    InternetService,
    COUNT(*) AS customers,
    SUM(ChurnFlag) AS churned,
    ROUND(AVG(ChurnFlag) * 100, 2) AS churn_rate_pct
FROM customers
GROUP BY InternetService
ORDER BY churn_rate_pct DESC;

-- 4. Churn by payment method
SELECT
    PaymentMethod,
    COUNT(*) AS customers,
    SUM(ChurnFlag) AS churned,
    ROUND(AVG(ChurnFlag) * 100, 2) AS churn_rate_pct
FROM customers
GROUP BY PaymentMethod
ORDER BY churn_rate_pct DESC;

-- 5. Customer tenure segmentation
SELECT
    CASE
        WHEN tenure < 12 THEN '0-11 months'
        WHEN tenure < 24 THEN '12-23 months'
        WHEN tenure < 48 THEN '24-47 months'
        ELSE '48+ months'
    END AS tenure_segment,
    COUNT(*) AS customers,
    SUM(ChurnFlag) AS churned,
    ROUND(AVG(ChurnFlag) * 100, 2) AS churn_rate_pct
FROM customers
GROUP BY tenure_segment
ORDER BY churn_rate_pct DESC;
