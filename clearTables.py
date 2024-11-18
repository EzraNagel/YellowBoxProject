from sqlalchemy import create_engine, text

# Database credentials
DB_USER = 'yellowbox_user'
DB_PASSWORD = 'password'
DB_HOST = 'localhost'
DB_PORT = '3306'
DB_NAME = 'yellowbox_db'

# Connect to the MySQL database
engine = create_engine(f'mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}')

# Clear all tables
def clear_tables():
    with engine.connect() as conn:
        conn.execute(text("SET FOREIGN_KEY_CHECKS = 0;"))
        tables = conn.execute(text("SHOW TABLES;")).fetchall()
        
        for table in tables:
            table_name = table[0]
            print(f"Dropping table: {table_name}")
            conn.execute(text(f"DROP TABLE IF EXISTS `{table_name}`;"))
        
        conn.execute(text("SET FOREIGN_KEY_CHECKS = 1;"))
        print("All tables cleared.")

if __name__ == "__main__":
    clear_tables()
