from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# Configure esta URL com suas credenciais de banco de dados PostgreSQL
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:lizard1240king@localhost/clinicas_db?options=-csearch_path%3Dpublic"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()