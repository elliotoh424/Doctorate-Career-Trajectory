# The PhD Job Market in Industry: A Data-Driven Analysis Using Revelio Data
This project analyses the private-sector career trajectory and competitive landscape for PhD graduates.

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
###

![Alt text](https://raw.githubusercontent.com/username/repo/main/images/plot.png)

