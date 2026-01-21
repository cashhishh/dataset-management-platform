"""
User and Dataset response schemas using Pydantic.
Defines data structures returned to API clients.
"""
from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional


class UserResponse(BaseModel):
    """Schema for user response (without password)"""
    id: int
    email: EmailStr
    username: str
    role: str
    created_at: datetime
    
    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "email": "john@example.com",
                "username": "johndoe",
                "role": "user",
                "created_at": "2026-01-21T10:30:00"
            }
        }


class DatasetCreate(BaseModel):
    """Schema for creating a new dataset"""
    name: str = Field(..., min_length=1, max_length=255)
    description: str
    file_path: Optional[str] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "name": "Customer Analysis Dataset",
                "description": "Dataset containing customer behavior data",
                "file_path": "/uploads/customer_data.csv"
            }
        }


class DatasetResponse(BaseModel):
    """Schema for dataset response"""
    id: int
    name: str
    description: str
    user_id: int
    file_path: Optional[str] = None
    created_at: datetime
    
    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "name": "Customer Analysis Dataset",
                "description": "Dataset containing customer behavior data",
                "user_id": 1,
                "file_path": "/uploads/customer_data.csv",
                "created_at": "2026-01-21T10:30:00"
            }
        }


class DatasetResponseWithOwner(BaseModel):
    """Schema for dataset response with owner information (admin view)"""
    id: int
    name: str
    description: str
    user_id: int
    file_path: Optional[str] = None
    created_at: datetime
    owner_username: str
    owner_email: EmailStr
    
    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "name": "Customer Analysis Dataset",
                "description": "Dataset containing customer behavior data",
                "user_id": 1,
                "file_path": "/uploads/customer_data.csv",
                "created_at": "2026-01-21T10:30:00",
                "owner_username": "johndoe",
                "owner_email": "john@example.com"
            }
        }
