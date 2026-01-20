from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from datetime import datetime
from app.services.user_service import UserService

router = APIRouter()
service = UserService()

class UserRequest(BaseModel):
    user_id: str
    name: str
    email: str
    phone: str

@router.get("/health")
def health():
    return {"status": "ok"}

@router.post("/user")
def create_user(user: UserRequest):
    created = service.create_user({
        "user_id": user.user_id,
        "name": user.name,
        "email": user.email,
        "phone": user.phone,
        "created_at": datetime.utcnow()
    })
    return created

@router.get("/user/{user_id}")
def get_user(user_id: str):
    user = service.get_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

