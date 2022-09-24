from datetime import datetime
from typing import Any
from dataclasses import dataclass
from pydantic import BaseModel
from typing import List, Optional

@dataclass
class InsightModel:
    account_uuid: str
    cloud_account_uuid: str
    event_id: str
    event_time: datetime
    event_level: str
    event_category: str
    error_message: str
    region: str
    username: str
    description: str
    request_id: str
    additional_data: Optional[List[dict]]

    @staticmethod
    def from_aws_dict(obj: Any,account_id:str,cloud_account_id:str) -> 'InsightModel':
        _event_id = str(obj.get("eventID"))
        _event_time = obj.get("eventTime")
        _event_level = obj.get("eventType")
        _event_category = str(obj.get("eventCategory"))
        _error_message = str(obj.get("errorMessage"))
        _username = str(obj.get("recipientAccountId"))
        _request_id = str(obj.get("requestID"))
        _region = str(obj.get("awsRegion"))
        _description = str(obj.get("errorCode"))+" "+str(obj.get("eventName"))
        _additional_data = [
            {"userIdentity": obj.get("userIdentity")},
            {"sourceIPAddress": obj.get("sourceIPAddress")},
            {"userAgent": obj.get("userAgent")}
            ]
        _account_uuid = account_id
        _cloud_account_uuid = cloud_account_id
        
        return InsightModel(_account_uuid,_cloud_account_uuid,_event_id,_event_time, _event_level, _event_category, _error_message, _region, _username, _description, _request_id, _additional_data)

    @staticmethod
    def from_azure_dict(obj: Any,account_id:str,cloud_account_id:str) -> 'InsightModel':
        _event_id = str(obj.get("eventDataId"))
        _event_time = obj.get("eventTimestamp")
        _event_level = obj.get("level")
        _event_category = str(obj.get("eventCategory",{}).get("value"))
        _error_message = str(obj.get("description"))
        _username = str(obj.get("recipientAccountId"))
        _request_id = str(obj.get("id"))
        _region = str(obj.get("properties",{}).get("region"))
        _description = str(obj.get("properties",{}).get("defaultLanguageContent"))
        _additional_data = [
            {"status": obj.get("status")},
            {"channels": obj.get("channels")},
            {"incidentType": obj.get("properties",{}).get("incidentType")},
            {"impactType": obj.get("properties",{}).get("impactType")},
            {"service": obj.get("service")},
            ]
        _account_uuid = account_id
        _cloud_account_uuid = cloud_account_id
        
        return InsightModel(_account_uuid,_cloud_account_uuid,_event_id,_event_time, _event_level, _event_category, _error_message, _region, _username, _description, _request_id, _additional_data)


class InsightCreateBaseModel(BaseModel):
    account_uuid: str
    cloud_account_uuid: str
    event_id: str
    event_time: datetime
    event_level: str
    event_category: str
    error_message: str
    region: str
    username: str
    description: str
    request_id: str
    additional_data: Optional[List[dict]]