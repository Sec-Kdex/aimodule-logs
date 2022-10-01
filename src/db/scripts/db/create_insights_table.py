import aurora_db
from dotenv import load_dotenv

def create_insights_table():
    commands = """
        CREATE TABLE IF NOT EXISTS insights (
            insight_id SERIAL PRIMARY KEY,
            account_uuid UUID NOT NULL,
            cloud_account_uuid UUID NOT NULL,
            event_id TEXT,
            event_time TIMESTAMP WITH TIME ZONE,
            event_level TEXT,
            event_category TEXT,
            error_message TEXT,
            region TEXT,
            username TEXT NOT NULL,
            description TEXT,
            request_id TEXT NOT NULL,
            additional_data json
        )
    """
    
    database_function = aurora_db.DatabaseFunction()
    database_function.create_table(commands=commands)
   

if __name__ == '__main__':
    load_dotenv()
    create_insights_table()
    
