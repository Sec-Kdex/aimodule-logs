from typing import Generator
from ..aurora.aurora_adaptor import SessionLocal

def get_db() -> Generator:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()