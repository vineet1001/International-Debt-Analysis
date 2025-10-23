# International Debt Analysis from The World Bank Data
---

## Overview

This repository contains an analysis of international debt data collected by **The World Bank**. The dataset provides information about the debt amount (in USD) owed by various developing countries across different debt categories (indicators).

The analysis is performed using **SQL**, focusing on extracting key statistics and insights into the global economic landscape concerning international borrowing.

## Project Goals

The primary objectives of this analysis were to answer fundamental questions about the dataset:

1. **Total Debt:** Determine the total amount of debt owed by all countries listed in the dataset.
2. **Maximum Debt:** Identify the country that owes the largest total amount of debt and the magnitude of that amount.
3. **Average Debt:** Calculate the average amount of debt owed by the countries across different debt indicators to understand distribution.

---

## Dataset

The analysis uses the \`international_debt\` dataset, which includes the following columns:

| Column Name | Description |
| :--- | :--- |
| \`country_name\` | Name of the country |
| \`country_code\` | Code for the country |
| \`indicator_name\` | Full name of the debt indicator/category |
| \`indicator_code\` | Code for the debt indicator/category |
| \`debt\` | Amount of debt owed (in current US\$) |

---

## Key Findings & Insights

The SQL analysis revealed several key facts about the international debt landscape:

| Question | SQL Query Summary | Result | Insight |
| :--- | :--- | :--- | :--- |
| **Total Debt** | \`SUM(debt)\` | **\$3,079,734.49\$ Million USD** | The collective debt is a colossal amount, indicating significant global reliance on borrowing. |
| **Country with Highest Debt** | \`SUM(debt) GROUP BY country_name ORDER BY total_debt DESC\` | **China**: \$285,793,494,734.2 USD | China is the single largest debtor in the dataset. |
| **Highest Average Debt Indicator** | \`AVG(debt) GROUP BY indicator_code ORDER BY average_debt DESC\` | **DT.AMT.DLXF.CD** (Principal repayments on external debt, long-term) | Repayment of long-term debt represents the highest average amount owed, suggesting this is a critical and high-value category of debt. |
| **Most Common Debt Indicators** | \`COUNT(indicator_code) GROUP BY indicator_code ORDER BY indicator_count DESC\` | Six indicators, including **DT.AMT.DLXF.CD**, are present for all **124** countries. | This shows a shared commonality in borrowing areas (e.g., official and multilateral debt, long-term principal and interest) across all developing nations in the dataset. |
| **Country with Highest Debt in *Any* Single Indicator** | \`MAX(debt) GROUP BY country_name\` | **China** (\$96.2 Billion USD) in the \`DT.AMT.DLXF.CD\` category. | Further emphasizes the large principal repayments China has under long-term debt. |

---
