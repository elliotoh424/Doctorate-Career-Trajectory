# Private-Sector Career Outcomes for PhD Graduates: Evidence from Revelio Labs Data
This project analyzes where PhD graduates actually work after graduation using Revelio Labs’ workforce data.

# Motivation
1.  **Tenure market is shrinking:** 50% decline in tenure-track roles since 2002.
2.  **Knowledge Gap:** PhDs lack knowledge on their private sector options.

## Summary
### Finding 1 — Collapse of the Tenure-Track Pathway
**50% decline** in the share of PhD graduates in tenure-track positions since 2002.
* Hard sciences are hit the hardest.
* Universities must benchmark programs against industry outcomes, not just academic placements.

![Tenure-Track Share Over Time](https://github.com/elliotoh424/Doctorate-Career-Trajectory/blob/main/figures/pct_tt_faculty_by_graduationyear.png)
![Tenure-Track Share Decline by Field](https://github.com/elliotoh424/Doctorate-Career-Trajectory/blob/main/figures/signed_pct_change_tt_2002_2024_by_field.png)

### Finding 2 — PhDs Cluster in Tech & Pharma
Graduates flood into Healthcare, Pharmaceuticals, IT, and Electronics.
* **Common roles:** Data Scientist, Software Engineer, Machine Learning Engineer.
* **Implication:** A Physics PhD is often competing directly against an Engineering PhD for the same "Data Scientist" role.
![Common Industries](https://github.com/elliotoh424/Doctorate-Career-Trajectory/blob/main/figures/top10_industries_nonacademic_since2002.png)
![Common Occupations](https://github.com/elliotoh424/Doctorate-Career-Trajectory/blob/main/figures/top10_occupations_nonacademic_since2002.png)

### Finding 3 — Fields are Surprisingly Distinct
Despite the "Data Science" boom, most fields have little overlap. High competition only exists in natural pairs:
* Medicine $\leftrightarrow$ Biology
* Economics $\leftrightarrow$ Finance
* Physics $\leftrightarrow$ Engineering

![Occupation Similarity Heatmap](https://github.com/elliotoh424/Doctorate-Career-Trajectory/blob/main/figures/field_similarity_heatmap_occ.png)

### Finding 4 — Each Field Has Clear Employment Niches
PhDs succeed most when targeting specific niches rather than generic roles. The table below shows the top 3 roles where each field has a comparative advantage.

**Top three occupations with most field representation:**

| Field | Top Occupations | % of Grads in Role |
| :--- | :--- | :--- |
| **Economics** | **Economist**, Credit Risk Analyst | 26.4% |
| **Statistics** | **Statistician**, Quantitative Analyst | 19.3% |
| **Physics** | **Quant Analyst**, Data Engineer | 4.5% |
| **Math** | **Quant Analyst**, Actuary | 10.2% |
| **Biology** | **Medical Writer**, Research Tech | 5.2% |
| **Chemistry** | **Research Chemist**, Chemist | 9.9% |
| **Engineering** | **Structural Engineer**, Petroleum Engineer | 1.2% |
| **Finance** | **Capital Markets**, Portfolio Manager | 1.8% |
| **IT** | **Info Security**, Network Admin | 2.2% |
| **Marketing** | **Marketing Consultant**, Analytics | 3.1% |
| **Accounting** | **Tax Accountant**, Financial Officer | 3.6% |

*(Full occupation list available in notebook)*

# Data & Methodology

**⚠️ Data Note:** This project uses **Revelio Labs** proprietary firm-position microdata.
* This repository **does not** contain underlying microdata.
* It contains the **code pipeline** and **aggregated figures** only.

**Methodology:**
1.  **Filter:** Exclude academic employers.
2.  **Similarity:** Calculated Cosine Similarity between occupation lists for different fields.
3.  **Advantage:** Calculated by normalizing the number of graduates in a specific role against the total market.


## 🔄 Pipeline Details
### Stage 1: Sample Construction (01_prepare_revelio_data.py)
Creates a matched sample of employees who obtained a PhD degree. Includes firm, industry, position, educational information for all PhD graduates.  

### Stage 2: Dataset Preparation (02_phd_careers_analysis.ipynb)
Generates figures and calculates cosine similarity by field.  