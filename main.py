from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import uvicorn
import firebase_admin
from firebase_admin import credentials, firestore
from firebase_admin.firestore import firestore as fs
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

# Load the service account key from the environment variable
private_key=os.getenv('private_key')
private_key_id=os.getenv('private_key_id')
client_email=os.getenv('client_email')
project_id=os.getenv('project_id')
client_id=os.getenv('client_id')
client_x509_cert_url=os.getenv('client_x509_cert_url')

cred_dict = {
  "type": "service_account",
  "project_id": project_id,
  "private_key_id": private_key_id,
  "private_key": private_key,
  "client_email": client_email,
  "client_id": client_id,
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": client_x509_cert_url,
  "universe_domain": "googleapis.com"
}

cred = credentials.Certificate(cred_dict)
firebase_admin.initialize_app(cred)
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