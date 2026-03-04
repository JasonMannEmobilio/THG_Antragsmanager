from fastapi import FastAPI, HTTPException, Header
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List, Any, Dict
import os
from dotenv import load_dotenv
import httpx

# Load .env from the same directory as this file
load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Allow all for now, restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

XANO_API_BASE_URL = os.getenv("XANO_API_BASE_URL")
# XANO_API_KEY removed as per request

# Models source of truth from user request
class Record(BaseModel):
    id: int
    created_at: int
    partner_id: Optional[str] = None
    external_reference: Optional[str] = None
    customer_number: Optional[str] = None
    license_plate: Optional[str] = None
    holder_name: Optional[str] = None
    registration_date: Optional[str] = None # date
    vehicle_class: Optional[str] = None
    vin: Optional[str] = None
    bonus_year: Optional[int] = None
    document_file: Optional[Any] = None
    document_filename: Optional[str] = None
    status: Optional[str] = None
    assigned_user_id: Optional[str] = None
    agent_notes: Optional[str] = None
    backend_reference: Optional[str] = None
    premium_amount_cents: Optional[int] = None
    payout_date: Optional[str] = None # date
    updated_at: int

class UpdateRecordInput(BaseModel):
    id: int
    status: Optional[str] = None
    premium_amount_cents: Optional[int] = None
    payout_date: Optional[str] = None
    assigned_user_id: Optional[int] = None

class LoginInput(BaseModel):
    email: str
    password: str

@app.get("/records")
async def get_records(authorization: Optional[str] = Header(None)):
    if not XANO_API_BASE_URL:
        # Return mock data if no env var
        return [
            {
                "id": 1,
                "created_at": 1678886400000,
                "partner_id": "P123",
                "holder_name": "John Doe",
                "status": "active",
                "premium_amount_cents": 5000,
                "payout_date": "2023-01-01"
            }
        ]
        
    async with httpx.AsyncClient() as client:
        # User defined endpoint: Intern_get
        headers = {}
        if authorization:
            headers["Authorization"] = authorization
            
        response = await client.get(f"{XANO_API_BASE_URL}/Intern_get", headers=headers) 
        if response.status_code >= 400:
            raise HTTPException(status_code=response.status_code, detail=response.text)
        return response.json()

@app.patch("/records")
async def update_record(input_data: UpdateRecordInput, authorization: Optional[str] = Header(None)):
    data = input_data.dict(exclude_unset=True)
    
    url = f"{XANO_API_BASE_URL}/Intern_patch"
    print(f"DEBUG: PATCH URL: {url}")
    print(f"DEBUG: PATCH DATA: {data}")
    
    if not XANO_API_BASE_URL:
        return {"status": "success", "data": data, "mock": True}

    async with httpx.AsyncClient() as client:
        # User defined endpoint: Intern_patch expects id in the body (input), not in the URL path.
        headers = {}
        if authorization:
            headers["Authorization"] = authorization
            
        response = await client.patch(f"{XANO_API_BASE_URL}/Intern_patch", json=data, headers=headers)
        if response.status_code >= 400:
            raise HTTPException(status_code=response.status_code, detail=response.text)
        return response.json()
@app.post("/login")
async def login(input_data: LoginInput):
    data = input_data.dict()
    
    if not XANO_API_BASE_URL:
        # Mock successful login if no Xano URL
        if data["email"] == "j.mann@e-mobilio.de" and data["password"] == "test":
             return {"authToken": "mock_token_123"}
        raise HTTPException(status_code=401, detail="Invalid credentials")

    async with httpx.AsyncClient() as client:
        # Xano auth login endpoint
        response = await client.post(f"{XANO_API_BASE_URL}/auth/login", json=data)
        if response.status_code >= 400:
            raise HTTPException(status_code=response.status_code, detail=response.text)
        return response.json()
