import os
from dotenv import load_dotenv
import psycopg2
import pandas as pd
from feature_selection import data_cleaning
from tfidf_approach import tfidf_vectorized_format
from sklearn.ensemble import IsolationForest
import joblib
from constants import FEATURE_COLS

def predict_score(logs_dict):
    df = pd.DataFrame.from_dict(logs_dict)
    print("got: ", len(df), "new logs")

    feature_df = df[FEATURE_COLS]

    cleaned_df = data_cleaning(feature_df)

    df_matrix = tfidf_vectorized_format(cleaned_df)

    model=IsolationForest(n_estimators=50, max_samples='auto', contamination=float(0.01),max_features=5)
    model.fit(df_matrix)

    t = model.predict(df_matrix)

    df['anomaly_score'] = t

    return df.to_dict('records')

if __name__ == "__main__":
    load_dotenv()

    DATABASE_URL= f"""host='{os.environ.get("DB_HOST")}' port='{os.environ.get("DB_PORT")}' dbname='{os.environ.get("DB_NAME")}' user='{os.environ.get("DB_USER")}' password='{os.environ.get("DB_PASSWORD")}'"""

    conn = psycopg2.connect(DATABASE_URL)

    conn.cursor().execute("SET search_path TO secdb")
    df = pd.read_sql("select * from insights", conn)

    print("read: ", len(df), "insight rows")

    feature_df = df[FEATURE_COLS]

    cleaned_df = data_cleaning(feature_df)

    df_matrix = tfidf_vectorized_format(cleaned_df)

    model=IsolationForest(n_estimators=50, max_samples='auto', contamination=float(0.01),max_features=5)
    model.fit(df_matrix)

    print("saving model as pkl")
    joblib.dump(model, 'anomaly_detection_model.pkl.pkl')
    print("!!! model saved !!!")

    m2 = joblib.load('anomaly_detection_model.pkl.pkl')
    print("model loaded")

    t = m2.predict([[0.1,0.4,0.23]])
    print(len(t))
