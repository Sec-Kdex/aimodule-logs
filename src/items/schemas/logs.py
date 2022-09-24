from ...db.aurora.aurora_model import Base
from sqlalchemy import Column, Integer, String,JSON, DATETIME
from sqlalchemy.dialects.postgresql import UUID

class InsightsSchema(Base):
    __tablename__ = "insights"

    insight_id = Column(Integer, primary_key=True) # Auto-increment should be default
    account_uuid = Column(String)
    cloud_account_uuid = Column(String)
    event_id = Column(String)
    event_time = Column(DATETIME)
    event_level = Column(String)
    event_category = Column(String)
    error_message = Column(String)
    region = Column(String)
    username = Column(String)
    description = Column(String)
    request_id = Column(String)
    additional_data = Column(JSON)
    