from sqlmodel import Session, create_engine
from dotenv import load_dotenv
import os

load_dotenv()

url = os.getenv("DB_URL")

engine = create_engine(url)

session = Session(engine)

def get_db():
    try:
        yield session
    except:
        session.rollback()
    finally:
        session.close()





