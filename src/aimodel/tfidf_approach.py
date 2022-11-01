import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd
import re
from ..aimodel.constants import MAX_DF, MIN_DF, DATA_CLEANING_TARGET_COLS, SYMBOLS, FEATURE_COLS
from nltk.corpus import stopwords
from nltk.stem import LancasterStemmer 

CLEANR = re.compile('<.*?>') 
STOPWORDS = stopwords.words('english')
ls = LancasterStemmer()

def cleanhtml(raw_html):
  clean_text = re.sub(CLEANR, '', raw_html)
  return clean_text

def sentence_preprocess(s):
    clean_str = cleanhtml(s)
   
    for i in SYMBOLS:
        clean_str = clean_str.replace(i, ' ')
    
    clean_str = s.replace("\n\t",  " ")
    clean_str = re.sub('[^a-zA-Z0-9 \n\.]', '', clean_str)
    clean_str = clean_str.lower()
    clean_str = clean_str.split(" ")
    clean_str = [ls.stem(item) for item in clean_str if item not in STOPWORDS]
    return list(set(clean_str))

def tfidf_vectorized_format(feature_df):
    formatted_df = feature_df
    vectorizer = TfidfVectorizer(stop_words='english',analyzer=lambda x: x,max_df=MAX_DF,min_df=MIN_DF)

    final_df = formatted_df

    for col in FEATURE_COLS: 
        
        formatted_df[col] = formatted_df[col].apply(sentence_preprocess)
 
        V_s = vectorizer.fit_transform(formatted_df[col]).toarray()

        t = pd.DataFrame(V_s,columns=vectorizer.get_feature_names_out())
    
        frames = [final_df, t]
    
        final_df = pd.concat(frames,axis=1)
        

    for col in FEATURE_COLS: 
        final_df.drop([col],axis=1,inplace=True)

    final_df.replace(np.nan, 0,inplace=True)
    final_df = final_df.groupby(level=0, axis=1).max()

    print("final tfidf dimension: ",final_df.shape)

    return final_df.to_numpy()