from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

load_dotenv()
def get_db_engine():
    try:
        user = os.environ["DB_USER"]
        pw = os.environ["DB_PASSWORD"]
        host = os.environ.get("DB_HOST", "localhost")
        port = int(os.environ.get("DB_PORT", 3306))
        db = os.environ["DB_NAME"]
        return create_engine(f"mysql+pymysql://{user}:{pw}@{host}:{port}/{db}?charset=utf8mb4")
    except KeyError as e:
        raise RuntimeError(f"[환경변수 누락] 확인: {e}")
