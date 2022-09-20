import aurora_db

def create_insights_table():
    commands = """
        CREATE TABLE insights (
            id_insights INT(11) NOT NULL AUTO_INCREMENT,
            created_at TIMESTAMP WITH TIME ZONE,
            error_message TEXT,
            region TEXT,
            username TEXT NOT NULL,
            description TEXT,
            request_id TEXT NOT NULL,
        )
    """
    
    database_function = aurora_db.DatabaseFunction()
    database_function.create_table(commands=commands)
   

if __name__ == '__main__':
    create_insights_table()
    
