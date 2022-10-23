from fastapi import APIRouter, Depends, HTTPException
from ..models.insights import InsightModel
from ..items.insights import InsightsCollection
from sqlalchemy.orm import Session
from ..db.aurora import auroradb
from dotenv import load_dotenv
from typing import Optional, Any
from pydantic import BaseModel

router = APIRouter()

load_dotenv()

class CloudLogs(BaseModel):
    aws_logs: Optional[Any] = None
    azure_logs: Optional[Any] = None


@router.post("/v1/insights/create")
async def create_insights(
    account_id: str,
    cloud_account_id: str,
    cloud_logs: CloudLogs,
    db: Session = Depends(auroradb.get_db)  
):
    try:
        logs = []

        if cloud_logs:
            cloud_logs_dict = cloud_logs.dict()
            
            if "aws_logs" in cloud_logs_dict.keys():
                if isinstance(cloud_logs_dict["aws_logs"],list):
                    for aws_event in cloud_logs_dict["aws_logs"]:
                        log = InsightModel.from_aws_dict(aws_event,account_id,cloud_account_id,0)
                        logs.append(log)

            if "azure_logs" in cloud_logs_dict.keys():
                if "responses" in cloud_logs_dict["azure_logs"].keys():
                    if isinstance(cloud_logs_dict["azure_logs"]["responses"],list):
                        if "content" in cloud_logs_dict["azure_logs"]["responses"][0].keys():
                            if "value" in cloud_logs_dict["azure_logs"]["responses"][0]["content"]["value"]:
                                if isinstance(cloud_logs_dict["azure_logs"]["responses"][0]["content"]["value"],list):
                                    for azure_event in cloud_logs_dict["azure_logs"]["responses"][0]["content"]["value"]:
                                        log = InsightModel.from_azure_dict(azure_event,account_id,cloud_account_id,0)
                                        logs.append(log)



        #call for prediction

        # insights_collection = InsightsCollection()  
    
        # return await insights_collection.add_insights(logs=logs,db=db)  
    
    except Exception as e:
        print("error: ",e)
        raise HTTPException(status_code=500, detail="Something went wrong while adding insights")