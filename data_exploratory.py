import requests
import pandas as pd
from sklearn.preprocessing import LabelEncoder

try:
   
    judge_api = requests.get('http://127.0.0.1:8000/judge/get_all_judges')
    judge_api.raise_for_status()
    judge_api_data = judge_api.json()

    performer_api = requests.get('http://127.0.0.1:8000/performer/get_all_performers')
    performer_api.raise_for_status()
    performer_api_data = performer_api.json()

    auditions_api = requests.get('http://127.0.0.1:8000/judge/get_all_auditions')
    auditions_api.raise_for_status()
    auditions_data = auditions_api.json()

    performances_api = requests.get('http://127.0.0.1:8000/judge/get_all_performances')
    performances_api.raise_for_status()
    performances_data = performances_api.json()

    
    judge_df = pd.DataFrame(judge_api_data["judges"])
    performer_df = pd.DataFrame(performer_api_data["performers"])
    auditions_df = pd.DataFrame(auditions_data["auditions"])
    performances_df = pd.DataFrame(performances_data["performances"])

    judge_df = judge_df.rename(columns={'id': 'judge_id', 'name': 'judge_name', 'email': 'judge_email'})
    performer_df = performer_df.rename(columns={'id': 'performer_id', 'name': 'performer_name', 'email': 'performer_email'})
    auditions_df = auditions_df.rename(columns={
        'id': 'audition_id',
        'title': 'audition_title',
        'description': 'audition_desc',
        'judge_id': 'judge_id'
    })
    performances_df = performances_df.rename(columns={
        'id': 'performance_id',
        'performer_id': 'performer_id',
        'audition_id': 'audition_id',
        'score': 'performance_score'
    })

    
    merged_df = pd.merge(performances_df, performer_df, on='performer_id', how='inner')
    merged_df = pd.merge(merged_df, auditions_df, on='audition_id', how='inner')
    merged_df = pd.merge(merged_df, judge_df, on='judge_id', how='inner')

    
    merged_df['audition_desc'].fillna('No description provided', inplace=True)

   
    if 'session_date' in merged_df.columns:
        merged_df['session_date'] = pd.to_datetime(merged_df['session_date'], errors='coerce')
        merged_df['session_year'] = merged_df['session_date'].dt.year
        merged_df['session_month'] = merged_df['session_date'].dt.month
        merged_df['session_day'] = merged_df['session_date'].dt.day
    else:
       
        merged_df['session_date'] = '2024-12-10'
        merged_df['session_year'] = 2024
        merged_df['session_month'] = 12
        merged_df['session_day'] = 10

   
    label_encoder = LabelEncoder()
    merged_df['judge_name_encoded'] = label_encoder.fit_transform(merged_df['judge_name'])
    merged_df['performer_name_encoded'] = label_encoder.fit_transform(merged_df['performer_name'])

  
    print("Merged DataFrame Info:")
    print(merged_df.info())
    print("\nMerged DataFrame Description:")
    print(merged_df.describe())
    print("\nMerged DataFrame Shape:")
    print(merged_df.shape)
    print("\nMerged DataFrame Head:")
    print(merged_df.head())

except requests.exceptions.RequestException as e:
    print(f"Error fetching data from API: {e}")

except Exception as e:
    print(f"An error occurred: {e}")
