from fastapi import APIRouter, Depends

from ..models.insights import InsightModel
from ..items.logs import LogInsightsCollection
from sqlalchemy.orm import Session
from ..db.aurora import auroradb
import json
import requests

router = APIRouter()

user_logs_req_url = 'http://54.226.103.69:3002/secdb/v1/acitivity/logs?accountID=21d9d6be-8078-49b7-aa43-74eac47851ad&type=aws&cloudAccountID=60248947-9f0b-4fc7-ac74-6c4d38c2b659'


@router.get("/logs/home")
async def root():
    return {"message": "Hello World"}

@router.put("/logs")
async def update_logs_insights(
    db: Session = Depends(auroradb.get_db)
):
    response = requests.get(user_logs_req_url)
    json_response = json.loads(response.text)

    logs = []

    for logJSON in json_response:
        log = InsightModel.from_aws_dict(logJSON)
        logs.append(log)

    insights_collection = LogInsightsCollection()  

    await insights_collection.upsert_insights(logs=logs,db=db)

    return logs