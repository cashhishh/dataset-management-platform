"""
Authentication routes for user registration and login.
Provides JWT-based authentication endpoints.
"""
from fastapi import APIRouter, HTTPException, status, Depends, Response
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import logging

from app.schemas.auth import UserRegister, UserLogin, Token, TokenData
from app.schemas.user import UserResponse
from app.models.user import UserModel
from app.core.security import verify_password, create_access_token, decode_access_token

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/auth", tags=["Authentication"])
security = HTTPBearer()


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(user_data: UserRegister):
    """
    Register a new user.
    - Ensures unique email and username
    - Hashes password before storing
    - Returns user info (without password)
    """

    # Check email uniqueness
    if UserModel.get_user_by_email(user_data.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    # Check username uniqueness
    if UserModel.get_user_by_username(user_data.username):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already taken"
        )

    # Create user
    user = UserModel.create_user(
        email=user_data.email,
        username=user_data.username,
        password=user_data.password,
        role=user_data.role
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create user"
        )

    logger.info(f"User registered: {user['email']}")
    return user


@router.post("/login", response_model=Token)
async def login(credentials: UserLogin, response: Response):
    """
    Authenticate user and return JWT token.
    """

    user = UserModel.get_user_by_email(credentials.email)

    if not user or not verify_password(credentials.password, user["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
            headers={"WWW-Authenticate": "Bearer"}
        )

    token_payload = {
        "sub": str(user["id"]),
        "role": user["role"]
    }

    access_token = create_access_token(token_payload)

    # Prevent response caching
    response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"

    logger.info(f"User logged in: {user['email']}")
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> TokenData:
    """
    Dependency to validate JWT token and extract user info.
    """

    payload = decode_access_token(credentials.credentials)

    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"}
        )

    user_id = payload.get("sub")
    role = payload.get("role")

    if user_id is None or role is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload",
            headers={"WWW-Authenticate": "Bearer"}
        )

    return TokenData(user_id=int(user_id), role=role)


async def require_admin(
    current_user: TokenData = Depends(get_current_user)
) -> TokenData:
    """
    Dependency to restrict access to admin users only.
    """
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )

    return current_user


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(
    current_user: TokenData = Depends(get_current_user)
):
    """
    Return current authenticated user's information.
    """

    user = UserModel.get_user_by_id(current_user.user_id)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    return user
