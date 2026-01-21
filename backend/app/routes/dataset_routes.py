"""
Dataset management routes with role-based access control.
Users can only manage their own datasets, admins can view all.
"""
from fastapi import APIRouter, HTTPException, status, Depends
from typing import List, Union
from app.schemas.user import DatasetCreate, DatasetResponse, DatasetResponseWithOwner
from app.schemas.auth import TokenData
from app.models.dataset import DatasetModel
from app.routes.auth_routes import get_current_user, require_admin
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/datasets", tags=["Datasets"])


@router.post("/", response_model=DatasetResponse, status_code=status.HTTP_201_CREATED)
async def create_dataset(
    dataset_data: DatasetCreate,
    current_user: TokenData = Depends(get_current_user)
):
    """
    Create a new dataset.
    
    - Authenticated users can create datasets
    - Dataset is automatically linked to the creating user
    """
    dataset = DatasetModel.create_dataset(
        name=dataset_data.name,
        description=dataset_data.description,
        user_id=current_user.user_id,
        file_path=dataset_data.file_path
    )
    
    if not dataset:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create dataset"
        )
    
    logger.info(f"Dataset created: {dataset['name']} by user {current_user.user_id}")
    return dataset


@router.get("/", response_model=Union[List[DatasetResponse], List[DatasetResponseWithOwner]])
async def get_datasets(current_user: TokenData = Depends(get_current_user)):
    """
    Get datasets based on user role.
    
    - Regular users: See only their own datasets
    - Admins: See all datasets with owner information
    """
    if current_user.role == "admin":
        # Admin sees all datasets with owner info
        datasets = DatasetModel.get_all_datasets()
        logger.info(f"Admin {current_user.user_id} retrieved all datasets")
    else:
        # Regular users see only their own datasets
        datasets = DatasetModel.get_datasets_by_user(current_user.user_id)
        logger.info(f"User {current_user.user_id} retrieved their datasets")
    
    return datasets


@router.get("/{dataset_id}", response_model=DatasetResponse)
async def get_dataset(
    dataset_id: int,
    current_user: TokenData = Depends(get_current_user)
):
    """
    Get a specific dataset by ID.
    
    - Users can only access their own datasets
    - Admins can access any dataset
    """
    dataset = DatasetModel.get_dataset_by_id(dataset_id)
    
    if not dataset:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Dataset not found"
        )
    
    # Authorization check: users can only access their own datasets
    if current_user.role != "admin" and dataset["user_id"] != current_user.user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: you can only view your own datasets"
        )
    
    return dataset


@router.delete("/{dataset_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_dataset(
    dataset_id: int,
    current_user: TokenData = Depends(get_current_user)
):
    """
    Delete a dataset.
    
    - Users can only delete their own datasets
    - Admins cannot delete other users' datasets (ownership protection)
    """
    # Check if dataset exists
    dataset = DatasetModel.get_dataset_by_id(dataset_id)
    
    if not dataset:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Dataset not found"
        )
    
    # Authorization: only owner can delete
    if dataset["user_id"] != current_user.user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: you can only delete your own datasets"
        )
    
    # Delete dataset
    success = DatasetModel.delete_dataset(dataset_id, current_user.user_id)
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete dataset"
        )
    
    logger.info(f"Dataset {dataset_id} deleted by user {current_user.user_id}")
    return None


@router.get("/admin/all", response_model=List[DatasetResponseWithOwner])
async def get_all_datasets_admin(admin_user: TokenData = Depends(require_admin)):
    """
    Admin-only endpoint to view all datasets with owner information.
    
    - Requires admin role
    - Returns comprehensive dataset list with user details
    """
    datasets = DatasetModel.get_all_datasets()
    logger.info(f"Admin {admin_user.user_id} retrieved all datasets via admin endpoint")
    return datasets
