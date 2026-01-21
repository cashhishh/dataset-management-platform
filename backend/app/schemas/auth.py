"""
Authentication request/response schemas using Pydantic.
Defines data validation for registration, login, and token responses.
"""
from pydantic import BaseModel, EmailStr, Field


class UserRegister(BaseModel):
    """Schema for user registration request"""
    email: EmailStr
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=6)
    role: str = Field(default="user", pattern="^(user|admin)$")
    
    class Config:
        json_schema_extra = {
            "example": {
                "email": "john@example.com",
                "username": "johndoe",
                "password": "securepass123",
                "role": "user"
            }
        }


class UserLogin(BaseModel):
    """Schema for user login request"""
    email: EmailStr
    password: str
    
    class Config:
        json_schema_extra = {
            "example": {
                "email": "john@example.com",
                "password": "securepass123"
            }
        }


class Token(BaseModel):
    """Schema for JWT token response"""
    access_token: str
    token_type: str = "bearer"
    
    class Config:
        json_schema_extra = {
            "example": {
                "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "token_type": "bearer"
            }
        }


class TokenData(BaseModel):
    """Schema for decoded token data"""
    user_id: int
    role: str
