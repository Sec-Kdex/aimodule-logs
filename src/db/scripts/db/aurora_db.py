import psycopg2
import os
import sys
import os
from dotenv import load_dotenv

load_dotenv()
# getting the name of the directory
# where the this file is present.
current = os.path.dirname(os.path.realpath(__file__))
# Getting the parent directory name
# where the current directory is present.
parent = os.path.dirname(current)
# adding the parent directory to
# the sys.path.
sys.path.append(parent)

DATABASE_URL = f"""host='{os.environ.get("DB_HOST")}' port={os.environ.get("DB_PORT")} dbname='{os.environ.get("DB_NAME")}' user='{os.environ.get("DB_USER")}' password='{os.environ.get("DB_PASSWORD")}'"""


class DatabaseFunction:
    def __init__(self) -> None:
        pass

    def create_table(self, commands: any):
        conn = None
        try:
            conn = psycopg2.connect(DATABASE_URL)
            cur = conn.cursor()
            cur.execute(commands)
            cur.close()
            conn.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()

    def create_function(self, commands: any):
        conn = None
        try:
            conn = psycopg2.connect(DATABASE_URL)
            cur = conn.cursor()
            cur.execute(commands)
            cur.close()
            conn.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()