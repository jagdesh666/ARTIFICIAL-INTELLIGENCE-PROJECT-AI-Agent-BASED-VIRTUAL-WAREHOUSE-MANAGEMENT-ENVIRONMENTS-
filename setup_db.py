from src.database.db_handler import DatabaseHandler

def setup():
    db = DatabaseHandler()
    # Schema script ka rasta
    db.execute_script('sql_scripts/schema.sql')
    db.close()

if __name__ == "__main__":
    setup()