import numpy as np
import pandas as pd
import wrds
import os
import re
import duckdb
import datetime
import matplotlib.pyplot as plt
from sklearn.metrics.pairwise import cosine_similarity

edu_file = 'C:/Users/elliotoh/Box/lodes_shared/revelio/individual_user_education_doctor.parquet'
eduraw_file = 'C:/Users/elliotoh/Box/lodes_shared/revelio/individual_user_education_raw_doctor.parquet'
position_file = 'C:/Users/elliotoh/Box/lodes_shared/revelio/individual_positions_doctor.parquet'
positionraw_file = 'C:/Users/elliotoh/Box/lodes_shared/revelio/individual_positions_raw_doctor.parquet'
user_file = 'C:/Users/elliotoh/Box/lodes_shared/revelio/individual_user_doctor.parquet'
userraw_file = 'C:/Users/elliotoh/Box/lodes_shared/revelio/individual_user_raw_doctor.parquet'
company_file = 'C:/Users/elliotoh/Box/lodes_shared/revelio/company_all.parquet'
school_file = 'C:/Users/elliotoh/Box/lodes_shared/revelio/school_mapping.parquet'
firmsize_file = 'C:/Users/elliotoh/Box/lodes_shared/revelio/firmsize.parquet'
homecountry_file = 'C:/Users/elliotoh/Box/lodes_shared/revelio/homecountry_doctor.parquet'
edu_merged_file = 'C:/Users/elliotoh/Box/lodes_shared/revelio/education_doctor_filtered.parquet'

db = wrds.Connection(wrds_username='rokman54')
db.list_tables('revelio')
# Query relevant data.

# Education processed
edu_query = """
    SELECT *
    FROM revelio.individual_user_education
    WHERE degree = 'Doctor';
"""
edu = db.raw_sql(edu_query)
edu.to_parquet(f"{edu_file}", index=False, compression='zstd')

# Education raw
edur_query = r"""
SELECT *
FROM revelio.individual_user_education_raw
WHERE upper(degree_raw) LIKE '%%DOCTOR%%' 
OR upper(degree_raw) LIKE '%%PHD%%';
"""
edur = db.raw_sql(edur_query)
edur.to_parquet(f"{eduraw_file}", index=False, compression='zstd')

con = duckdb.connect()

edu = con.sql(f"SELECT * FROM '{edu_file}'").df()
eduraw = con.sql(f"SELECT * FROM '{eduraw_file}'").df()
# edu.create_view("edu")
# eduraw.create_view("eduraw")

school_query = """
    SELECT *
    FROM revelio.school_mapping
"""
school_mapping = db.raw_sql(school_query)
school_mapping.to_parquet(f"{school_file}", index=False, compression='zstd')

#
id_list = pd.read_parquet(edu_merged_file, columns = ['user_id'])['user_id'].unique().tolist()
ids_formatted = ",".join(f"'{x}'" for x in id_list)

db = wrds.Connection(wrds_username='rokman54')
# Checked whether filling missing enddate with current date is good idea. Checked around 60. Most missing enddates is because it is listed as "Present".
homecountry_query = f"""
    WITH earliest AS(
    SELECT edu.user_id, MIN(edu.startdate) AS earliest_startdate
    FROM revelio.individual_user_education as edu
    WHERE edu.user_id IN ({ids_formatted})
    GROUP BY edu.user_id
    )
    SELECT edu.user_id, edu.rsid, edu.degree, edu.field, edu.education_number, earliest.earliest_startdate, edu.startdate, edu.enddate, school.country, school.state, school.metro_area
    FROM revelio.individual_user_education as edu
    JOIN earliest
    ON edu.user_id = earliest.user_id
    JOIN revelio.school_mapping as school
    ON edu.rsid = school.rsid
    WHERE edu.user_id IN ({ids_formatted})
    AND edu.startdate <= earliest.earliest_startdate
    """
homecountry = db.raw_sql(homecountry_query) # 957714 users out of 1013534
homecountry.user_id.nunique()
#
edur_query1 = f"""
SELECT *
FROM revelio.individual_user_education_raw
WHERE user_id IN ({ids_formatted});
"""
edur1 = db.raw_sql(edur_query1)
#
homecountry= homecountry.merge(edur1, on=['user_id','education_number'])
homecountry[homecountry[['user_id','education_number']].duplicated()]
#
homecountry = homecountry.merge(school_mapping, on=['rsid'])
# 41020 user_id with multiple user_id-earliestcountry pairs out of 957714 user_id. Just get earliest country
homecountry.sort_values(['user_id','country_y'], inplace=True)
homecountry.user_id.duplicated().sum()
homecountry.user_id.nunique()
homecountry = homecountry.groupby('user_id').first().reset_index()
homecountry = homecountry[['user_id','country_y']]
homecountry.columns = ['user_id','homecountry']
homecountry.user_id.duplicated().sum()
homecountry.to_parquet(f"{homecountry_file}", index=False, compression='zstd')

# Position
position_query = f"""
    SELECT *
    FROM revelio.individual_positions
    WHERE user_id IN ({ids_formatted})
"""
position = db.raw_sql(position_query)
position.to_parquet(f"{position_file}", index=False, compression='zstd')

positionraw_query = f"""
    SELECT *
    FROM revelio.individual_positions_raw
    WHERE user_id IN ({ids_formatted})
"""
positionraw = db.raw_sql(positionraw_query)
positionraw.to_parquet(f"{positionraw_file}", index=False, compression='zstd')

user_query = f"""
    SELECT *
    FROM revelio.individual_user
    WHERE user_id IN ({ids_formatted})
"""
user = db.raw_sql(user_query)
user.to_parquet(f"{user_file}", index=False, compression='zstd')

userraw_query = f"""
    SELECT *
    FROM revelio.individual_user_raw
    WHERE user_id IN ({ids_formatted})
"""
userraw = db.raw_sql(userraw_query)
userraw.to_parquet(f"{userraw_file}", index=False, compression='zstd')

company_query = f"""
    SELECT *
    FROM revelio.company_mapping
"""
company = db.raw_sql(company_query)
company.to_parquet(f"{company_file}", index=False, compression='zstd')

phd_firms = pd.read_parquet('C:/Users/elliotoh/Box/lodes_shared/revelio/phd_company_rcid.parquet') 
phd_firms = phd_firms.rcid.unique().tolist()
phd_ids_formatted = ",".join(f"'{x}'" for x in phd_firms)

db = wrds.Connection(wrds_username='rokman54')

# Checked whether filling missing enddate with current date is good idea. Checked around 60. Most missing enddates is because it is listed as "Present".
firmsize_query = f"""
    SELECT rcid, COUNT(DISTINCT user_id) AS employees_2025
    FROM revelio.individual_positions
    WHERE rcid IN ({phd_ids_formatted})
    AND startdate IS NOT NULL
    AND startdate <= '2025-12-31'
    AND (enddate IS NULL OR enddate >= '2025-01-01')
    GROUP BY rcid
"""
firmsize = db.raw_sql(firmsize_query)
firmsize.to_parquet(f"{firmsize_file}", index=False, compression='zstd')



# Read and process files
# Has start and end dates
# Has school name
phd_edu = pd.read_parquet(edu_file) # 10515517
phd_edu = phd_edu[phd_edu.university_name.notnull()]
phd_edu = phd_edu[phd_edu.startdate.notnull() & phd_edu.enddate.notnull()] # 7761549 (74% remains)
phd_edu['startdate'] = pd.to_datetime(phd_edu['startdate'])
phd_edu['enddate'] = pd.to_datetime(phd_edu['enddate'])
phd_edu = phd_edu[phd_edu.enddate >= phd_edu.startdate]
phd_edu = phd_edu[phd_edu.enddate <= pd.Timestamp.today()] # 7240118
phd_edu = phd_edu[phd_edu.enddate>='1980-01-01'] # 7031151
phd_edu = phd_edu[phd_edu.startdate>='1980-01-01'] # 6887155
phd_edu[phd_edu[['user_id','education_number']].duplicated()]
# 
all_school = pd.read_parquet(school_file)
all_school[all_school.rsid.duplicated()]
phd_edu = phd_edu.merge(all_school[['rsid','school_name','school_cleaned','country','state','city','metro_area']], on='rsid')
phd_edu.rename(columns = {'startdate':'phd_startdate', 'enddate':'phd_enddate', 'country':'phd_country','state':'phd_state','city':'phd_city','metro_area':'phd_metro_area'}, inplace=True)
phd_edu= phd_edu[phd_edu.phd_country=='United States'] # 3268063 remaining
# Raw file has field of study
phd_eduraw = pd.read_parquet(eduraw_file)
phd_eduraw[phd_eduraw[['user_id','education_number']].duplicated()]
#
phd_edu_merged = phd_edu.merge(phd_eduraw, on=['user_id','education_number']) # University names match well
phd_edu_merged['degree_cleaned'] = phd_edu_merged['degree_raw'].str.upper().str.replace('\(.+\).*$', '', regex=True)
phd_edu_merged['degree_cleaned'] = phd_edu_merged['degree_cleaned'].str.upper().str.replace('-.*$', '', regex=True)
# Remove professional degrees
prof_degrees = [
    'DOCTORA?T?E? OF MEDICINE',
    'DOCTORA?T?E? OF LAW',
    'DOCTORA?T?E? OF PHARMACY',
    'DOCTORA?T?E? OF PHYSICAL THERAPY',
    'DOCTORA?T?E? OF VETERINARY MEDICINE',
    'DOCTORA?T?E? OF NURSING PRACTICE',
    'DOCTORA?T?E? OF DENTAL SURGERY',
    'DOCTORA?T?E? OF EDUCATION',
    'DOCTORA?T?E? OF CHIROPRACTIC',
    'DOCTORA?T?E? OF DENTAL MEDICINE',
    'DOCTORA?T?E? EN MEDICINA',
    'DOCTORA?T?E? OF PSYCHOLOGY',
    'DOCTORA?T?E? OF OCCUPATIONAL THERAPY',
    'DOCTORA?T?E? OF OPTOMETRY',
    'DOCTORA?T?E? OF AUDIOLOGY',
    'DOCTORA?T?E? OF OSTEOPATHIC MEDICINE',
    'DOCTORA?T?E? OF MINISTRY',
    'JURIS DOCTORA?T?E?',
    'MEDICAL DOCTORA?T?E?',
    'POSTDOCTOR',
    'POST DOCTOR',
    'VISITING PHD STUDENT'
]
phd_edu_merged = phd_edu_merged[~phd_edu_merged['degree_cleaned'].str.contains('|'.join(prof_degrees),na=False)] # Phd graduates drop off in 2025. Probably not everyone updated their linkedin or actually graduated yet (december graduates).
keep_cols = ['user_id', 'education_number', 'phd_startdate', 'phd_enddate', 'university_name', 'rsid', 'degree', 'degree_cleaned','field', 'field_raw', 
             'phd_state', 'phd_city', 'phd_metro_area',
             'description', 'degree_raw']
phd_edu_merged = phd_edu_merged[keep_cols]
# Exclude doctorates without any field info. Only 3.7%. Find that many clinical doctorates still in sample.
phd_edu_merged = phd_edu_merged[(phd_edu_merged.field.notnull()) | (phd_edu_merged.field_raw.notnull())]
drop_by_field = phd_edu_merged[phd_edu_merged.field.str.contains('Nursing|Law')].index # Drop fields where clinical/professional doctorate and research phd are hard to distinguish
phd_edu_merged = phd_edu_merged.drop(drop_by_field,axis=0)
drop_by_fieldraw = phd_edu_merged[phd_edu_merged.field_raw.str.contains('Nursing|Law|Physical Therapy|Therapist|Clinical Psychology|Counseling Psychology|Chiropractic|School Psychology|Osteopathic Medicine|Naturopathic Medicine|Podiatric Medicine|Veterinary Medicine|Dental Medicine')].index # Drop fields where clinical/professional doctorate and research phd are hard to distinguish
phd_edu_merged = phd_edu_merged.drop(drop_by_fieldraw,axis=0)
drop_by_fieldraw = phd_edu_merged[phd_edu_merged.field_raw.isin(['Medicine','Acupuncture and Oriental Medicine','Classical Chinese Medicine'])].index # Drop fields where clinical/professional doctorate and research phd are hard to distinguish
phd_edu_merged = phd_edu_merged.drop(drop_by_fieldraw,axis=0)
drop_by_degreeraw = phd_edu_merged[phd_edu_merged.degree_raw.str.contains('Naturopathic Medicine|Osteopathy|Podiatic Medicine|Naturopathic Medicine|Naturopathic Doctor|Acupuncture|Oriental Medicine|Dental Medicine|Podiatric Medicine|Naturopathy|Plant Medicine|Doctor of Medicine|Nursing Practice|Plant Medicine|Natuopathic Medicine',na=False, flags=re.IGNORECASE)].index # Drop fields where clinical/professional doctorate and research phd are hard to distinguish
phd_edu_merged = phd_edu_merged.drop(drop_by_degreeraw,axis=0)
phd_edu_merged.to_parquet(edu_merged_file, index=False, compression='zstd')

# Positions
phd_edu_final_id = phd_edu_merged.user_id.unique().tolist()
phd_position = pd.read_parquet(position_file, filters = [('user_id', 'in', phd_edu_final_id)])
cols = ['region','country','state','metro_area','city','startdate','enddate']
phd_position = phd_position.rename(columns={c: f'position_{c}' for c in cols})
phd_position[phd_position[['user_id','position_id']].duplicated()]
#
phd_positionraw = pd.read_parquet(positionraw_file, filters = [('user_id', 'in', phd_edu_final_id)])
phd_positionraw[phd_positionraw[['user_id','position_id']].duplicated()]
phd_position_merged = phd_position.merge(phd_positionraw, on=['user_id','position_id'])
phd_position_merged[phd_position_merged[['user_id','position_id']].duplicated()]
# 
# Use user update times to fill in missing end dates.
phd_user = pd.read_parquet(user_file, filters = [('user_id', 'in', phd_edu_final_id)], columns = ['user_id','updated_dt','profile_linkedin_url','fullname'])
phd_position_merged = phd_position_merged.merge(phd_user, on='user_id', how='left')
phd_position_merged.updated_dt.isnull().sum()
# Have checked that most empty enddates are because it is "to Present".
phd_position_merged.loc[(phd_position_merged.position_enddate.isnull()),'position_enddate'] = phd_position_merged.loc[(phd_position_merged.position_enddate.isnull()),'updated_dt']
keep_cols = ['user_id', 'position_id', 'position_region', 'position_country', 'position_state', 'position_metro_area', 'msa', 'position_city',
             'position_startdate', 'position_enddate', 'role_k1500_v2', 'role_k17000_v3', 'remote_suitability', 'weight', 'start_salary', 'end_salary', 
             'seniority', 'salary', 'position_number', 'rcid', 'ultimate_parent_rcid', 'onet_code', 'total_compensation', 'additional_compensation', 
             'company_raw', 'location_raw', 'title_raw','description', 'profile_linkedin_url']
phd_position_merged = phd_position_merged[keep_cols]
phd_position_merged = phd_position_merged[phd_position_merged.position_startdate.notnull() & phd_position_merged.position_enddate.notnull()]
# companies
phd_firm_id = phd_position_merged[phd_position_merged.rcid.notnull()].rcid.unique().tolist()
phd_company = pd.read_parquet(company_file, filters = [('rcid','in',phd_firm_id)])
phd_company[['rcid']].drop_duplicates().to_parquet('C:/Users/elliotoh/Box/lodes_shared/revelio/phd_company_rcid.parquet', index=False, compression='zstd') 
#
keep_cols = ['rcid', 'company', 'year_founded', 'ticker', 'gvkey',  'exchange_name', 'url',  
       'naics_code', 'rics_k50', 'rics_k200', 'rics_k400', 
       'linkedin_url', 'hq_region', 'hq_country', 'hq_metro_area',  
       'hq_street_address', 'hq_city',  'hq_state', 'hq_zip_code', 
       'description']
phd_company = phd_company[keep_cols]
# 
phd_position_merged = phd_position_merged.merge(phd_company, on='rcid', how='left')
phd_position_merged.rename(columns={'description_x':'position_description', 'description_y':'company_description','linkedin_url':'company_linkedin_url'}, inplace=True)
keep_cols = [
        'user_id', 'position_id', 'position_region', 'position_country', 'position_state', 'position_metro_area', 'position_city',
       'position_startdate', 'position_enddate', 'role_k1500_v2', 'role_k17000_v3', 'remote_suitability', 'weight', 
       'start_salary', 'end_salary', 'seniority', 'salary', 'position_number', 'onet_code', 
       'total_compensation', 'additional_compensation', 'company_raw', 'location_raw', 'title_raw',
       'position_description', 'profile_linkedin_url', 
       'rcid', 'company', 'year_founded', 'ticker', 'gvkey', 'exchange_name', 'url', 'naics_code',
       'rics_k50', 'rics_k200', 'rics_k400', 'company_linkedin_url', 
       'hq_region', 'hq_country', 'hq_metro_area', 'hq_street_address', 'hq_city', 'hq_state', 'hq_zip_code', 'company_description'
]
phd_position_merged = phd_position_merged[keep_cols]
phd_position_merged[phd_position_merged[['user_id','position_id']].duplicated()]
# Now we have user-position-firm info. Now just merge with phd info.
phd_position_merged = phd_position_merged.merge(phd_edu_merged, on =['user_id'])
phd_position_merged['position_startdate'] = pd.to_datetime(phd_position_merged.position_startdate)
phd_position_merged['position_enddate'] = pd.to_datetime(phd_position_merged.position_enddate)
phd_position_merged['nposition'] = phd_position_merged.groupby('user_id')['position_id'].transform('count')
phd_position_merged = phd_position_merged[phd_position_merged.nposition>=3] # At least 3 positions. Removes 4.7%
phd_position_merged['phd_cohortyear'] = phd_position_merged.phd_enddate.dt.year
# 
# Combine with # of employee info as of 2025.
firmsize25 = pd.read_parquet(firmsize_file)
phd_position_merged = phd_position_merged.merge(firmsize25, on='rcid',how='left') # Most left merges are positions without rcids
#
cols = ['user_id','homecountry']
homecountry = pd.read_parquet(homecountry_file, columns = cols)
phd_position_merged = phd_position_merged.merge(homecountry, on='user_id',how='left') # 48543 unmatched.
# Merge with O*NET titles
onet = pd.read_excel('C:/Users/elliotoh/Box/lodes_shared/revelio/Occupation Data.xlsx')
onet.columns = ['onet_code','onet_title','description']
onet = onet[['onet_code','onet_title']]
phd_position_merged = phd_position_merged.merge(onet, on='onet_code', how='left')
phd_position_merged.sort_values(['user_id','position_startdate','position_enddate','position_number'], inplace=True)
phd_position_merged.to_parquet('C:/Users/elliotoh/Box/lodes_shared/revelio/phd_position_merged.parquet', index=False, compression='zstd')

# Post-phd positions
phd_position_merged = pd.read_parquet('C:/Users/elliotoh/Box/lodes_shared/revelio/phd_position_merged.parquet')
postphd_positions = phd_position_merged[phd_position_merged.position_startdate > phd_position_merged.phd_enddate]
postphd_positions.reset_index(drop=True, inplace=True)
postphd_positions['postphd_position_number'] = postphd_positions.groupby(['user_id']).cumcount()
postphd_positions['postphd_total_position'] = postphd_positions.groupby('user_id')['position_id'].transform('count')
postphd_positions.to_parquet('C:/Users/elliotoh/Box/lodes_shared/revelio/phd_careers.parquet', index=False, compression='zstd')

