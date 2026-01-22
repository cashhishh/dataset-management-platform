"""
Pydantic schemas for dataset operations.
"""
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime


class DatasetCreate(BaseModel):
    """Schema for creating a dataset (without file upload)"""
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None


class DatasetUpload(BaseModel):
    """Schema for dataset upload response"""
    name: str
    description: Optional[str] = None


class DatasetResponse(BaseModel):
    """Schema for dataset response"""
    id: int
    name: str
    description: Optional[str]
    user_id: int
    file_path: Optional[str]
    file_name: Optional[str]
    file_size: Optional[int]
    row_count: Optional[int]
    column_count: Optional[int]
    created_at: datetime
    
    class Config:
        from_attributes = True


class DatasetWithOwner(DatasetResponse):
    """Schema for dataset with owner information (admin view)"""
    owner_username: str
    owner_email: str


class ColumnMetadata(BaseModel):
    """Schema for column metadata"""
    id: Optional[int] = None
    column_name: str
    column_type: str
    column_index: int


class QualityReport(BaseModel):
    """Schema for quality report"""
    id: Optional[int] = None
    total_rows: int
    total_columns: int
    duplicate_rows: int
    null_counts: Dict[str, int]
    completeness_score: float
    generated_at: Optional[datetime] = None


class DatasetDetail(BaseModel):
    """Schema for detailed dataset view"""
    dataset: DatasetResponse
    columns: List[ColumnMetadata]
    quality_report: Optional[QualityReport]


class DatasetPreview(BaseModel):
    """Schema for dataset preview"""
    columns: List[str]
    rows: List[Dict[str, Any]]
    total_rows: int
