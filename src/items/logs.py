from http.client import HTTPException
from ..models.insights import InsightModel, InsightCreateBaseModel
from sqlalchemy.orm import Session
from .schemas.logs import InsightsSchema
from typing import List
from ..db.aurora.aurora_base import CRUDBase

class LogInsightsCollection:
    def __init__(self) -> None:
        self.model = CRUDBase(InsightsSchema)

    async def upsert_insights(
        self,
        logs: List[InsightModel],
        db: Session
    ) -> any:
        try:
            created_logs = []
            for log in logs:
                #log_create = InsightCreateBaseModel(**log.dict())
                created_log= self.model.create(db=db, obj_in=log)
                
                created_logs.append(created_log)

            return created_logs
    
        except Exception:
            raise HTTPException(status_code=500, detail="Something went wrong updating the logs")
