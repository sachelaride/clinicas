from sqlalchemy import create_engine, inspect
from app.core.database import SQLALCHEMY_DATABASE_URL

engine = create_engine(SQLALCHEMY_DATABASE_URL)

def check_clinicas_table():
    inspector = inspect(engine)
    if 'clinicas' in inspector.get_table_names():
        print("Table 'clinicas' exists in the database.")
    else:
        print("Table 'clinicas' DOES NOT exist in the database.")

if __name__ == "__main__":
    check_clinicas_table()