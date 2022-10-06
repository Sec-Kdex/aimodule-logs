from typing import Generator
from ..aurora.aurora_adaptor import SessionLocal

def get_db() -> Generator:
    db = SessionLocal()
    db.execute("SET search_path TO secdb")
    try:
        yield db
    finally:
        db.close()