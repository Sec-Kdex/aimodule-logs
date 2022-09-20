import uvicorn
from fastapi import FastAPI
import json
import requests

user_logs_req_url = 'http://127.0.0.1/8080/sec/vi/'

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/userlogs")
async def use_requests(api_url):
    response = requests.get(api_url)
    json_response = json.loads(response.text)

    return json_response

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)