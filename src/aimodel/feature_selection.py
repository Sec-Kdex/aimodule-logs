import re
from constants import DATA_CLEANING_TARGET_COLS, SYMBOLS


def cleanhtml(raw_html):
    CLEANR = re.compile('<.*?>') 
    
    clean_text = re.sub(CLEANR, '', raw_html)
    return clean_text

def data_cleaning(feature_df):
    clean_df = feature_df
    for col in DATA_CLEANING_TARGET_COLS:
        clean_df[col] = feature_df[col].str.lower()
  
    regex_constant = r'\buser: arn:aws:iam::\d*:user[/]\w*'
    regex_user_constant = r'\buser (\w+)'

    clean_df['error_message'] = clean_df['error_message'].str.replace(regex_constant, 'user *')
    clean_df['error_message'] = clean_df['error_message'].str.replace(regex_user_constant, 'user *')

    for i in SYMBOLS:
        clean_df['error_message'] = clean_df['error_message'].str.replace(i, ' ')

    clean_df['description'] = clean_df['description'].apply(cleanhtml)

    return clean_df