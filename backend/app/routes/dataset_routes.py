"""
Dataset management routes with role-based access control.
Users can only manage their own datasets, admins can view all.
"""

from fastapi import APIRouter, HTTPException, status, Depends, UploadFile, File, Form
from typing import List, Union, Optional
import logging

from app.schemas.dataset_schemas import (
    DatasetCreate,
    DatasetResponse,
    DatasetWithOwner,
    DatasetDetail,
    DatasetPreview,
    QualityReport
)
from app.schemas.auth import TokenData
from app.models.dataset import DatasetModel
from app.routes.auth_routes import get_current_user, require_admin
from app.services.file_service import save_upload_file, delete_file
from app.services.csv_parser import CSVParser

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/datasets", tags=["Datasets"])


@router.post("/", response_model=DatasetResponse, status_code=status.HTTP_201_CREATED)
async def create_dataset(
    dataset_data: DatasetCreate,
    current_user: TokenData = Depends(get_current_user)
):
    dataset = DatasetModel.create_dataset(
        name=dataset_data.name,
        description=dataset_data.description,
        user_id=current_user.user_id
    )

    if not dataset:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create dataset"
        )

    return dataset


@router.post("/upload", response_model=DatasetResponse, status_code=status.HTTP_201_CREATED)
async def upload_dataset(
    file: UploadFile = File(...),
    name: str = Form(...),
    description: Optional[str] = Form(None),
    current_user: TokenData = Depends(get_current_user)
):
    logger.info("=" * 60)
    logger.info(f"DATASET UPLOAD STARTED - User: {current_user.user_id}, File: {file.filename}")
    logger.info("=" * 60)

    file_path = None
    dataset = None

    try:
        # 1️⃣ Save file
        file_path, original_filename, file_size = await save_upload_file(
            file, current_user.user_id
        )

        # 2️⃣ Parse CSV
        parse_result = CSVParser.parse_csv_file(file_path)
        df = parse_result["df"]

        # 3️⃣ Quality analysis
        quality_data = CSVParser.analyze_data_quality(df)

        # 4️⃣ Create dataset
        dataset = DatasetModel.create_dataset(
            name=name,
            description=description,
            user_id=current_user.user_id,
            file_path=file_path,
            file_name=original_filename,
            file_size=file_size,
            row_count=parse_result["row_count"],
            column_count=parse_result["column_count"],
        )

        if not dataset:
            raise RuntimeError("Dataset DB insert failed")

        # 5️⃣ Save column metadata (FAIL = FULL ROLLBACK)
        if not DatasetModel.save_column_metadata(
            dataset["id"], parse_result["columns"]
        ):
            raise RuntimeError("Column metadata save failed")

        # 6️⃣ Save quality report (FAIL = FULL ROLLBACK)
        if not DatasetModel.save_quality_report(
            dataset["id"],
            quality_data["total_rows"],
            quality_data["total_columns"],
            quality_data["duplicate_rows"],
            quality_data["null_counts"],
            quality_data["completeness_score"],
        ):
            raise RuntimeError("Quality report save failed")

        logger.info("=" * 60)
        logger.info(f"DATASET UPLOAD COMPLETE - ID: {dataset['id']}")
        logger.info("=" * 60)

        return dataset

    except Exception as e:
        logger.error(f"Upload failed: {e}", exc_info=True)

        # 🔥 FULL CLEANUP (CRITICAL FIX)
        if dataset:
            DatasetModel.delete_dataset(dataset["id"], current_user.user_id)

        if file_path:
            delete_file(file_path)

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Dataset upload failed"
        )


@router.get("/", response_model=Union[List[DatasetResponse], List[DatasetWithOwner]])
async def get_datasets(current_user: TokenData = Depends(get_current_user)):
    if current_user.role == "admin":
        return DatasetModel.get_all_datasets()
    return DatasetModel.get_datasets_by_user(current_user.user_id)


@router.get("/{dataset_id}", response_model=DatasetResponse)
async def get_dataset(
    dataset_id: int,
    current_user: TokenData = Depends(get_current_user)
):
    dataset = DatasetModel.get_dataset_by_id(dataset_id)

    if not dataset:
        raise HTTPException(status_code=404, detail="Dataset not found")

    if current_user.role != "admin" and dataset["user_id"] != current_user.user_id:
        raise HTTPException(status_code=403, detail="Access denied")

    return dataset


@router.get("/{dataset_id}/detail", response_model=DatasetDetail)
async def get_dataset_detail(
    dataset_id: int,
    current_user: TokenData = Depends(get_current_user)
):
    dataset = DatasetModel.get_dataset_by_id(dataset_id)
    if not dataset:
        raise HTTPException(status_code=404, detail="Dataset not found")

    if current_user.role != "admin" and dataset["user_id"] != current_user.user_id:
        raise HTTPException(status_code=403, detail="Access denied")

    return {
        "dataset": dataset,
        "columns": DatasetModel.get_column_metadata(dataset_id),
        "quality_report": DatasetModel.get_quality_report(dataset_id),
    }


@router.get("/{dataset_id}/preview", response_model=DatasetPreview)
async def get_dataset_preview(
    dataset_id: int,
    limit: int = 10,
    current_user: TokenData = Depends(get_current_user)
):
    dataset = DatasetModel.get_dataset_by_id(dataset_id)
    if not dataset:
        raise HTTPException(status_code=404, detail="Dataset not found")

    if current_user.role != "admin" and dataset["user_id"] != current_user.user_id:
        raise HTTPException(status_code=403, detail="Access denied")

    rows = CSVParser.get_preview_data(dataset["file_path"], limit)
    columns = list(rows[0].keys()) if rows else []

    return {
        "columns": columns,
        "rows": rows,
        "total_rows": dataset.get("row_count", 0),
    }


@router.get("/{dataset_id}/quality", response_model=QualityReport)
async def get_quality_report(
    dataset_id: int,
    current_user: TokenData = Depends(get_current_user)
):
    dataset = DatasetModel.get_dataset_by_id(dataset_id)
    if not dataset:
        raise HTTPException(status_code=404, detail="Dataset not found")

    if current_user.role != "admin" and dataset["user_id"] != current_user.user_id:
        raise HTTPException(status_code=403, detail="Access denied")

    report = DatasetModel.get_quality_report(dataset_id)
    if not report:
        raise HTTPException(status_code=404, detail="Quality report not found")

    return report


@router.get("/admin/all", response_model=List[DatasetWithOwner])
async def get_all_datasets_admin(
    admin_user: TokenData = Depends(require_admin)
):
    return DatasetModel.get_all_datasets()
