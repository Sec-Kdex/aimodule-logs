from dataclasses import dataclass
from fastapi import APIRouter, Depends
import os
from ..models.insights import InsightModel
from ..items.logs import LogInsightsCollection
from sqlalchemy.orm import Session
from ..db.aurora import auroradb
import json
import requests
from dotenv import load_dotenv

router = APIRouter()

load_dotenv()

@router.put("/userlogs/account_id/{account_id}/cloud_account_id/{cloud_account_id}")
async def update_logs_insights(
    account_id: str,
    cloud_account_id: str,
    db: Session = Depends(auroradb.get_db)
):
    # user_logs_aws_req_url = f'''{os.environ.get("USER_LOGS_URL")}accountID={account_id}&type=aws&cloudAccountID={cloud_account_id}'''
    # response = requests.get(user_logs_aws_req_url)
    # json_response = json.loads(response.text)

    # logs = []

    # for logJSON in json_response:
    #     log = InsightModel.from_aws_dict(logJSON,account_id,cloud_account_id)
    #     logs.append(log)

    insights_collection = LogInsightsCollection()  

    # await insights_collection.upsert_insights(logs=logs,db=db)

    user_logs_azure_req_url = f'''{os.environ.get("USER_LOGS_URL")}accountID={account_id}&type=azure&cloudAccountID={cloud_account_id}'''

    f = open('C:/Users/Downloads/azure_logs.json','r',encoding="utf8")
    
    json_azure_data = json.load(f)
    azure_logs = []

    for logJSON in json_azure_data["responses"][0]["content"]["value"]:
        log = InsightModel.from_azure_dict(logJSON,account_id,cloud_account_id)
        azure_logs.append(log)
    
    await insights_collection.upsert_insights(logs=azure_logs,db=db)

    return azure_logs