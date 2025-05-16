from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import List
import bcrypt, jwt

app = FastAPI()
SECRET_KEY = "your_secret_key_here"

users = {"1234567890123": {
    "name": "John Doe",
    "password": bcrypt.hashpw("password123".encode(), bcrypt.gensalt()).decode(),
    "leaves": []
}}

class LoginInput(BaseModel):
    citizen_id: str
    password: str

class LeaveRequest(BaseModel):
    leave_type: str
    start_date: str
    end_date: str
    reason: str

@app.post("/login")
def login(data: LoginInput):
    user = users.get(data.citizen_id)
    if user and bcrypt.checkpw(data.password.encode(), user['password'].encode()):
        token = jwt.encode({"sub": data.citizen_id}, SECRET_KEY, algorithm="HS256")
        return {"token": token}
    raise HTTPException(status_code=401, detail="Invalid credentials")

@app.get("/leaves")
def get_leaves():
    return users["1234567890123"]["leaves"]

@app.post("/leaves")
def submit_leave(req: LeaveRequest):
    users["1234567890123"]["leaves"].append(req.dict())
    return {"message": "Leave submitted"}
