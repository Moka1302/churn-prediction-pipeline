CREATE TABLE features AS
SELECT
    "Customer ID" AS customer_id,
    Gender,
    CASE WHEN "Under 30" = 'Yes' THEN 1 ELSE 0 END AS under_30,
    CASE WHEN "Senior Citizen" = 'Yes' THEN 1 ELSE 0 END AS is_senior,
    CASE WHEN Married = 'Yes' THEN 1 ELSE 0 END AS has_partner,
    CASE WHEN Dependents = 'Yes' THEN 1 ELSE 0 END AS has_dependents,
    "Number of Dependents" AS num_dependents,
    "Referred a Friend" AS referred_friend,
    "Number of Referrals" AS num_referrals,
    "Tenure in Months" AS tenure_months,
    "Avg Monthly Long Distance Charges" AS avg_long_dist_charge,
    "Avg Monthly GB Download" AS avg_gb_download,
    "Monthly Charge" AS monthly_charge,
    "Total Charges" AS total_charges,
    "Total Refunds" AS total_refunds,
    "Total Extra Data Charges" AS total_extra_data,
    "Total Long Distance Charges" AS total_long_dist,
    "Total Revenue" AS total_revenue,
    "Satisfaction Score" AS satisfaction_score,
    -- tenure group
    CASE 
        WHEN "Tenure in Months" < 12 THEN 'short'
        WHEN "Tenure in Months" BETWEEN 12 AND 24 THEN 'medium'
        ELSE 'long'
    END AS tenure_group,
    -- contract and payment encoding
    CASE WHEN Contract LIKE '%Month%' THEN 1 ELSE 0 END AS is_month_to_month,
    CASE WHEN "Paperless Billing" = 'Yes' THEN 1 ELSE 0 END AS paperless,
    CASE WHEN lower("Payment Method") LIKE '%automatic%' THEN 1 ELSE 0 END AS is_auto_payment,
    -- count active services
    (
        (CASE WHEN "Phone Service"='Yes' THEN 1 ELSE 0 END) +
        (CASE WHEN "Multiple Lines"='Yes' THEN 1 ELSE 0 END) +
        (CASE WHEN "Online Security"='Yes' THEN 1 ELSE 0 END) +
        (CASE WHEN "Online Backup"='Yes' THEN 1 ELSE 0 END) +
        (CASE WHEN "Device Protection Plan"='Yes' THEN 1 ELSE 0 END) +
        (CASE WHEN "Premium Tech Support"='Yes' THEN 1 ELSE 0 END) +
        (CASE WHEN "Streaming TV"='Yes' THEN 1 ELSE 0 END) +
        (CASE WHEN "Streaming Movies"='Yes' THEN 1 ELSE 0 END) +
        (CASE WHEN "Streaming Music"='Yes' THEN 1 ELSE 0 END) +
        (CASE WHEN "Unlimited Data"='Yes' THEN 1 ELSE 0 END)
    ) AS num_services,
    "Churn Label" AS churn
FROM raw;

SELECT * FROM features;
