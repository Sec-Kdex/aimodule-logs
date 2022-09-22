import uvicorn
from fastapi import FastAPI
from src.routers import logs
from src.db.aurora.aurora_adaptor import SessionLocal

user_logs_req_url = 'http://54.226.103.69:3002/secdb/v1/acitivity/logs?accountID=21d9d6be-8078-49b7-aa43-74eac47851ad&type=aws&cloudAccountID=60248947-9f0b-4fc7-ac74-6c4d38c2b659'

app = FastAPI()

app.add_event_handler("startup", SessionLocal)

app.include_router(logs.router)

if __name__ == "__main__":
    print("running app on: 8000")
    uvicorn.run(app, host="127.0.0.1", port=8000)