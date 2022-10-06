from fastapi import APIRouter, Depends
import os
from ..models.insights import InsightModel
from ..items.insights import InsightsCollection
from sqlalchemy.orm import Session
from ..db.aurora import auroradb
import json
import requests
from dotenv import load_dotenv

router = APIRouter()

load_dotenv()

@router.put("/userlogs/accounts/{account_id}/cloud_accounts/{cloud_account_id}")
async def update_logs_insights(
    account_id: str,
    cloud_account_id: str,
    db: Session = Depends(auroradb.get_db)
):
    logs = []
    user_logs_aws_req_url = f'''{os.environ.get("USER_LOGS_URL")}accountID={account_id}&type=aws&cloudAccountID={cloud_account_id}'''
    response = requests.get(user_logs_aws_req_url)
    if response.text != None:
        json_response = json.loads(response.text)

        for aws_logs_JSON in json_response:
            log = InsightModel.from_aws_dict(aws_logs_JSON,account_id,cloud_account_id)
            logs.append(log)

    user_logs_azure_req_url = f'''{os.environ.get("USER_LOGS_URL")}accountID={account_id}&type=azure&cloudAccountID={cloud_account_id}'''
    azure_response = requests.get(user_logs_azure_req_url)
    
    if azure_response.text != None and azure_response.text != "":
        try:
            json_azure_data = json.loads(azure_response.text)
            
            if json_azure_data != "" and json_azure_data != None:
                if "responses" in json_azure_data.keys():
                    for aws_logs_JSON in json_azure_data["responses"][0]["content"]["value"]:
                        log = InsightModel.from_azure_dict(aws_logs_JSON,account_id,cloud_account_id)
                        logs.append(log)
        except:
            pass

    insights_collection = InsightsCollection()  
    
    await insights_collection.upsert_insights(logs=logs,db=db)

    return "logs updated successfully"