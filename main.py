from fastapi import FastAPI, Request
from fastapi.responses import PlainTextResponse, JSONResponse
import uvicorn
import firebase_admin
from firebase_admin import credentials, firestore
from firebase_admin.firestore import firestore as fs

app = FastAPI()
# Initialize the app with a service account, granting admin privileges
cred = credentials.Certificate('wappsender-key.json')
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
        return PlainTextResponse(content="Unsupported content type", status_code=415)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)