import uvicorn
from fastapi import FastAPI
from routers import insights
from src.db.aurora.aurora_adaptor import SessionLocal
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI()

app.add_event_handler("startup", SessionLocal)

app.include_router(insights.router)

if __name__ == "__main__":
    host = os.environ.get("HOST_URL")
    port = int(os.environ.get("PORT"))

    print("running app on: ",port)
    uvicorn.run(app, host=host, port=port)