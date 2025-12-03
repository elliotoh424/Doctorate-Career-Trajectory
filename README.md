# Private-Sector Career Outcomes for PhD Graduates: Evidence from Revelio Labs Data
What careers do PhD graduates have after graduation? This project analyzes private-sector career outcomes for PhD graduates across academic fields, using Revelio Labs’ firm-position microdata. 

# Motivation
1. Shrinking Tenure-Track market
2. PhDs lack knowledge on private sector
3. Importance of understanding field differences
4. Value of Revelio’s labor-flow data

## Summary
### Finding 1 — Collapse of the Tenure-Track Pathway
50% decline in share of PhD graduates with tenure-track positions since 2002. Hard sciences hit hardest. Universities and policymakers need to benchmark PhD program outcomes.
![Tenure-Track Share Over Time](https://github.com/elliotoh424/Doctorate-Career-Trajectory/blob/main/figures/pct_tt_faculty_by_graduationyear.png)
![Tenure-Track Share Decline by Field](https://github.com/elliotoh424/Doctorate-Career-Trajectory/blob/main/figures/signed_pct_change_tt_2002_2024_by_field.png)

### Finding 2 — PhDs Cluster into a Handful of Industries & Occupations
PhDs commonly enter Healthcare, pharma, IT, and electronics industry and commonly work as data scientists, software engineers, and machine engineers. PhDs may be competing against PhDs from different fields. 

![Common Industries](https://github.com/elliotoh424/Doctorate-Career-Trajectory/blob/main/figures/top10_industries_nonacademic_since2002.png)
![Common Occupations](https://github.com/elliotoh424/Doctorate-Career-Trajectory/blob/main/figures/top10_occupations_nonacademic_since2002.png)

### Finding 3 — But Fields Are Surprisingly Distinct (Low Cosine Similarity)
Similarity score analysis reveals that most field have little occupational overlap with other fields. High similarities only in natural pairs: medicine–biology, economics–finance, physics–engineering, and math–statistics.

![Occupation Similarity Heatmap](https://github.com/elliotoh424/Doctorate-Career-Trajectory/blob/main/figures/field_similarity_heatmap_occ.png)

### Finding 4 — Each Field Has Clear Employment Niches
Instead of chasing generic roles ('data scientist'), PhDs succeed more often when they pursue occupations aligned with field specialization. Biology → medical writer, Math → actuary, Physics → data engineer. Below table display the top three occupations with most field representation. 

| Field                 | Occupation                   | # Graduates from Field | # Graduates | % Graduates from Field |
|-----------------------|------------------------------|-------------------------|-------------|--------------------------|
| Accounting            | tax accountant               | 31                      | 155         | 0.034254                 |
| Accounting            | accounting                   | 33                      | 360         | 0.036464                 |
| Accounting            | financial officer            | 32                      | 685         | 0.035359                 |
| Architecture          | project architect            | 45                      | 117         | 0.025952                 |
| Architecture          | architect                    | 471                     | 1346        | 0.271626                 |
| Architecture          | architecture                 | 94                      | 279         | 0.054210                 |
| Biology               | medical writer               | 1522                    | 6431        | 0.047463                 |
| Biology               | technical support            | 30                      | 129         | 0.000936                 |
| Biology               | research technician          | 1679                    | 7246        | 0.052359                 |
| Business              | finance controller           | 39                      | 65          | 0.000809                 |
| Business              | contracts administrator      | 80                      | 138         | 0.001660                 |
| Business              | financial accounting         | 42                      | 73          | 0.000872                 |
| Chemistry             | research chemist             | 3954                    | 5530        | 0.099407                 |
| Chemistry             | chemist                      | 2430                    | 3421        | 0.061092                 |
| Chemistry             | analytical chemist           | 1783                    | 3115        | 0.044826                 |
| Economics             | economist                    | 6356                    | 8450        | 0.264734                 |
| Economics             | tax consultant               | 43                      | 81          | 0.001791                 |
| Economics             | credit risk analyst          | 101                     | 289         | 0.004207                 |
| Education             | admissions                   | 260                     | 1650        | 0.013752                 |
| Education             | counselor                    | 1238                    | 8199        | 0.065478                 |
| Education             | superintendent               | 218                     | 1470        | 0.011530                 |
| Engineering           | structural engineer          | 3034                    | 3256        | 0.012640                 |
| Engineering           | process control engineer     | 82                      | 93          | 0.000342                 |
| Engineering           | petroleum engineer           | 591                     | 678         | 0.002462                 |
| Finance               | capital markets              | 62                      | 418         | 0.017584                 |
| Finance               | portfolio                    | 52                      | 393         | 0.014748                 |
| Finance               | risk analyst                 | 32                      | 277         | 0.009075                 |
| Information Technology | network administrator       | 40                      | 302         | 0.017490                 |
| Information Technology | information security engineer | 51                    | 415         | 0.022300                 |
| Information Technology | cyber security              | 37                      | 652         | 0.016178                 |
| Marketing             | marketing research           | 44                      | 598         | 0.027604                 |
| Marketing             | marketing consultant         | 49                      | 937         | 0.030740                 |
| Marketing             | analytics                    | 44                      | 2358        | 0.027604                 |
| Mathematics           | actuarial                    | 115                     | 250         | 0.007457                 |
| Mathematics           | actuary                      | 116                     | 378         | 0.007522                 |
| Mathematics           | quantitative analyst         | 1577                    | 8072        | 0.102257                 |
| Medicine              | physician                    | 955                     | 14053       | 0.235512                 |
| Medicine              | medical                      | 277                     | 5362        | 0.068311                 |
| Medicine              | physical therapist           | 119                     | 2378        | 0.029346                 |
| Physics               | devops engineer              | 39                      | 261         | 0.001488                 |
| Physics               | data engineer                | 296                     | 2008        | 0.011296                 |
| Physics               | quantitative analyst         | 1171                    | 8072        | 0.044690                 |
| Statistics            | statistical programmer       | 400                     | 1512        | 0.038175                 |
| Statistics            | statistician                 | 2022                    | 8149        | 0.192976                 |
| Statistics            | quantitative analyst         | 904                     | 8072        | 0.086276                 |

### What This Means (for PhDs, universities, employers)
Employers do not view PhDs homogenously and each field has a distinct comparative advantage. By targetting field-specific roles, job seekers have a better chance of employment. Universities and policymakers need to inform which occupations best align with field.

# Data
Revelio Labs data provides provides firm-position level information for each individual along with education, occupation, and industry information. This repository **does not** contain the underlying data. Anyone with access to Revelio Labs data can replicate this notebook. 

# Methodology
1. Data filtering: Exclude academic employers from sample.
2. Similarity score: Cosine similarity between occupation weights for each field pair excluding itself.
3. Comparative advantage: # of graduates from field in occupation / # of graduates in occupation.

## 🔄 Pipeline Details
### Stage 1: Sample Construction (01_prepare_revelio_data.py)
Creates a matched sample of employees who obtained a PhD degree. Includes firm, industry, position, educational information for all PhD graduates.  

### Stage 2: Dataset Preparation (02_phd_careers_analysis.ipynb)
Generates figures and calculates cosine similarity by field.  