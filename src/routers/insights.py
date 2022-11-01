from fastapi import APIRouter, Depends, HTTPException
import json
from ..models.insights import InsightModel
from ..items.insights import InsightsCollection
from sqlalchemy.orm import Session
from ..db.aurora import auroradb
from dotenv import load_dotenv
from typing import Optional, Any
from pydantic import BaseModel
from ..aimodel.predict import predict_score

router = APIRouter()

load_dotenv()

class CloudLogs(BaseModel):
    aws_logs: Optional[Any] = None
    azure_logs: Optional[Any] = None


@router.post("/v1/insights/file")
async def create_insights(
    db: Session = Depends(auroradb.get_db)  
):
    logs = []

    #read the file
    azure_file = open('C:/Users/manis/Downloads/azure_logs.json','r',encoding="utf8")

    json_azure_data = json.load(azure_file)

    azure_account_id = "21d9d6be-8078-49b7-aa43-74eac47851ad"
    azure_cloud_account_id = "1f680352-c01b-443f-b9ac-f821ac757023"
    for azure_logs_JSON in json_azure_data["responses"][0]["content"]["value"]:
        log = InsightModel.from_azure_dict(azure_logs_JSON,azure_account_id,azure_cloud_account_id,0)
        logs.append(log)

    aws_file = open('C:/Users/manis/Downloads/aws_logs.json','r',encoding="utf8")
    json_aws_data = json.load(aws_file)

    aws_account_id = "21d9d6be-8078-49b7-aa43-74eac47851ad"
    aws_cloud_account_id = "60248947-9f0b-4fc7-ac74-6c4d38c2b659"
    for aws_logs_JSON in json_aws_data:
        log = InsightModel.from_aws_dict(aws_logs_JSON,aws_account_id,aws_cloud_account_id,0)
        logs.append(log)

    insights_collection = InsightsCollection() 

    print("db operation next")


    try: 
        await insights_collection.add_insights(logs=logs,db=db)
        print("successfully updated " + len(logs) + "logs")
    except Exception as e:
        print("error: ",e)
        raise Exception(e)

@router.post("/v1/insights/create")
async def create_insights(
    account_id: str,
    cloud_account_id: str,
    cloud_logs: CloudLogs,
    db: Session = Depends(auroradb.get_db)  
):
    logs = []

    if cloud_logs:
        cloud_logs_dict = cloud_logs.dict()
            
        if "aws_logs" in cloud_logs_dict.keys():
            if isinstance(cloud_logs_dict["aws_logs"],list):
                for aws_event in cloud_logs_dict["aws_logs"]:
                    try:
                        log = InsightModel.from_aws_dict(aws_event,account_id,cloud_account_id,0)
                        logs.append(log)
                    except:
                        pass
        print("got azure logs: ", cloud_logs_dict.keys())
        if "azure_logs" in cloud_logs_dict.keys() and cloud_logs_dict["azure_logs"]:
            print("got azure logs: ", type(cloud_logs_dict["azure_logs"]))
            if "responses" in cloud_logs_dict["azure_logs"].keys():
                print("cleared responses")
                if isinstance(cloud_logs_dict["azure_logs"]["responses"],list):
                    print("cleared list: ", type(cloud_logs_dict["azure_logs"]["responses"][0]))
                    if "content" in cloud_logs_dict["azure_logs"]["responses"][0].keys():
                        print("cleared content value")
                        if "value" in cloud_logs_dict["azure_logs"]["responses"][0]["content"]:
                            print("cleared content value", )
                            if isinstance(cloud_logs_dict["azure_logs"]["responses"][0]["content"]["value"],list):
                                print("final looping next")
                                for azure_event in cloud_logs_dict["azure_logs"]["responses"][0]["content"]["value"]:
                                    try:
                                
                                        log = InsightModel.from_azure_dict(azure_event,account_id,cloud_account_id,0)
                                      
                                        logs.append(log)

                                    except Exception as e:
                                        print("failed conversion azure: ",e)
                                        pass
                                print("total added: ", len(cloud_logs_dict["azure_logs"]["responses"][0]["content"]["value"]))

    #call for prediction

    log_insights = predict_score(logs)

    try:
        insights_collection = InsightsCollection()  
    
        return await insights_collection.add_insights(logs=log_insights,db=db)  
    
    except Exception as e:
        print("error: ",e)
        raise HTTPException(status_code=500, detail="Something went wrong while adding insights")