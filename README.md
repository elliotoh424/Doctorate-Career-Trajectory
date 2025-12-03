# Private-Sector Career Outcomes for PhD Graduates: Evidence from Revelio Labs Data
What careers do PhD graduates have after graduation? This project analyzes private-sector career outcomes for PhD graduates across academic fields, using Revelio Labs’ firm-position microdata. I visualize outcomes by industry, occupation, and company. I quantify cross-field competition for jobs based on cosine similarity scores. 

# How to Read This Notebook
This notebook has four short analytical sections:
1. Industry outcomes by field
2. Occupation outcomes by field
3. Employer outcomes by field
4. Cross-field similarity (cosine similarity analysis)

# What questions the notebook answers: 
    What percent of PhDs work in the private sector?
    Where do PhDs work at? What industries, occupations, and companies?
    Do PhDs from different fields compete against each other?
# Methodology
Exclude individuals with academic jobs. Calculate weighted average cosine similarity for each field. High similarity score means high level of competition with other fields.
# Answer: 
    30-70% of graduates work in academia. Substantial difference by field.
    Substantial overlap in industry and occupation among graduates from different field.
    PhD grads from different fields compete for same jobs (Many fields have high similarity scores). 
    Companies put little emphasis on domain expertise when hiring PhD graduates. Data scientist in finance = data scientist in tech.   

# Data
Revelio Labs data provides provides firm-position level information for each individual along with ducation, occupation, and industry information. Because Revelio Labs data is proprietary, this repository **does not** contain the underlying microdata. Anyone with access to Revelio Labs data can replicate this notebook. Instead, this notebook presents **fully executed code and figures** that were run locally with licensed access.

## 🔄 Pipeline Details
### Stage 1: Sample Construction (01_prepare_revelio_data.py)
Creates a matched sample of employees who obtained a PhD degree. Includes firm, industry, position, educational information for all PhD graduates.  

### Stage 2: Dataset Preparation (02_phd_careers_analysis.ipynb)
Generates figures and calculates cosine similarity by field.  

## Summary
Substantial different share of graduates who remain in academia. 70+% of accounting, education, and marketing PhD graduates stay in academic or research-oriented roles. Around half remain for architecture, finance, mathematics, economics, business, and physics. In hard sciences, only 30% remain. 

![Shares of Graduates in Academia by Field](https://github.com/elliotoh424/Doctorate-Career-Trajectory/blob/main/figures/pct_academia_alljobs_postphd_2010.png)

### By Industry
Many graduates enter into tech, healthcare, pharmaceuticals, and finance. Tech hires from sciences, engineering, math, and business programs. Healthcare and pharmaceuticals hires from biology, chemistry, medicine. Graduates from finance, economics, and mathematics enter into finance. 

### By Occupation
Data scientists, quantitative researchers, and software engineers comes from wide range of fields. Suggests that PhDs from different fields may compete with each other.
Data scientist: engineering, biology, statistician, physics, mathematics, economics. 
Quantitative analyst: physics, statistics, economics, mathematics, and finance. 
Machine engineer and software engineers: engineering, physics, mathematics, and information technology. 

### By Company 
Large tech companies and government institutions hire from wide range of fields.
Large tech companies: all fields except biology, chemistry, education, medicine, and accounting.
Government: business, education, medicine, finance, and accounting. 
Large pharma: biology and chemistry
Economic consulting: economics and finance
Semiconductor companies: engineering and physics
Finance: statistics, mathematics, finance.

### Competition among Phds from different fields
Cosine similarity scores show that PhD graduates across fields work in similar industries and occupations and compete for same jobs.

By Occupation
field	weighted_cosine_similarity	n_grads	top1_field	top1_sim
Physics	0.519783	20168	Mathematics	0.961095
Mathematics	0.490581	12279	Physics	0.961095
Statistics	0.354852	8682	Mathematics	0.842643
Biology	0.298329	24198	Medicine	0.600837
Engineering	0.292028	182747	Physics	0.716104
Information Technology	0.271463	2128	Engineering	0.355313
Chemistry	0.24054	29309	Biology	0.437107
Business	0.227899	44628	Education	0.706154
Marketing	0.205864	1435	Business	0.492931
Finance	0.174187	2642	Economics	0.931049
Economics	0.172346	17740	Finance	0.931049
Education	0.158096	19651	Business	0.706154
Medicine	0.142741	3486	Biology	0.600837
Accounting	0.095412	1105	Economics	0.663341
Architecture	0.049174	1519	Business	0.097774

### No distinction for domain expertise
Industry-occupation score is similar to occupation score in most fields. Companies recruit based on skill sets rather than domain expertise, effectively treating a data scientist in finance as identical to one in tech.

| Field                   | Weighted Cosine Similarity | n_grads | Top 1 Field | Top 1 Sim |
|------------------------|-----------------------------|---------|-------------|-----------|
| Physics                | 0.527093                    | 17,930  | Mathematics | 0.89047   |
| Mathematics            | 0.456673                    | 10,988  | Physics     | 0.89047   |
| Statistics             | 0.295609                    | 7,931   | Mathematics | 0.762719  |
| Engineering            | 0.283001                    | 161,056 | Physics     | 0.692458  |
| Information Technology | 0.246712                    | 1,656   | Engineering | 0.347083  |
| Chemistry              | 0.244420                    | 25,379  | Biology     | 0.398051  |
| Biology                | 0.225077                    | 19,860  | Medicine    | 0.683894  |
| Business               | 0.197213                    | 30,333  | Education   | 0.687775  |
| Finance                | 0.165963                    | 1,832   | Economics   | 0.727996  |
| Medicine               | 0.136125                    | 2,542   | Biology     | 0.683894  |
| Marketing              | 0.130945                    | 794     | Statistics  | 0.255651  |
| Economics              | 0.129540                    | 14,793  | Finance     | 0.727996  |
| Education              | 0.119081                    | 9,222   | Business    | 0.687775  |
| Accounting             | 0.065175                    | 501     | Finance     | 0.242085  |
| Architecture           | 0.030274                    | 986     | Business    | 0.041195  |

### Same holds within firm. 
Firm-occupation similarity score also very similar. PhDs from different fields also compete for same roles in same firms  

field	weighted_cosine_similarity	n_grads	top1_field	top1_sim
Physics	0.498651	18975	Engineering	0.71449
Mathematics	0.472483	11574	Engineering	0.714003
Engineering	0.267058	171707	Physics	0.71449
Chemistry	0.257456	26989	Physics	0.410661
Biology	0.211622	21095	Medicine	0.340396
Statistics	0.18474	8134	Mathematics	0.451837
Education	0.157952	12417	Business	0.70963
Business	0.151663	38092	Education	0.70963
Information Technology	0.144056	1850	Business	0.230698
Finance	0.13209	2152	Economics	0.456313
Marketing	0.118584	1003	Business	0.379264
Accounting	0.106648	628	Business	0.419981
Medicine	0.101933	2952	Education	0.364667
Economics	0.073622	16019	Finance	0.456313
Architecture	0.051428	1206	Business	0.129098



# Answer: 
    30-70% of graduates work in academia. Substantial difference by field.
    Substantial overlap in industry and occupation among graduates from different field.
    PhD grads from different fields compete for same jobs (Many fields have high similarity scores). 
    Companies put little emphasis on domain expertise when hiring PhD graduates. Data scientist in finance = data scientist in tech.   

## 🔄 Pipeline Details
### Stage 1: Sample Construction (01_prepare_revelio_data.py)
Creates a matched sample of employees who obtained a PhD degree. Includes firm, industry, position, educational information for all PhD graduates.  

### Stage 2: Dataset Preparation (02_phd_careers_analysis.ipynb)
Generates figures and calculates cosine similarity by field.  

