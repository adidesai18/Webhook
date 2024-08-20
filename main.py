from fastapi import FastAPI, Request
from fastapi.responses import PlainTextResponse, JSONResponse
import uvicorn
import firebase_admin
from firebase_admin import credentials, firestore
from firebase_admin.firestore import firestore as fs
import os
import json
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

# Load the service account key from the environment variable
service_account_info = os.getenv('GOOGLE_APPLICATION_CREDENTIALS_JSON')

if service_account_info:
    cred = credentials.Certificate(json.loads(service_account_info))
    firebase_admin.initialize_app(cred)
else:
    raise ValueError("No service account info found in environment variable.")

db = firestore.client()

@app.post("/")
async def receive_webhook(request: Request):
    # Determine the content type
    content_type = request.headers.get('Content-Type')

    if content_type == 'application/json':
        data = await request.json()
        db.collection('WappSender').document('message-ids').update({
            'ids': fs.ArrayUnion([data['data']['id']])
        })
        return JSONResponse(content={"message": "JSON received"})
    else:
        return JSONResponse(content={"message": "Unsupported content type"})

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)