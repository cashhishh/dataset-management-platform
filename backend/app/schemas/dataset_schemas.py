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


class NumericStats(BaseModel):
    """Numeric statistics for a column"""
    min: float
    max: float
    mean: float
    median: float
    std: float


class OutlierInfo(BaseModel):
    """Outlier detection information"""
    outlier_count: int
    outlier_percentage: float
    lower_bound: Optional[float]
    upper_bound: Optional[float]
    outliers: List[float]


class ColumnQualityReport(BaseModel):
    """Quality report for a single column"""
    column_name: str
    total_values: int
    null_count: int
    null_percentage: float
    empty_string_count: int
    empty_percentage: float
    invalid_count: int
    unique_count: int
    unique_percentage: float
    completeness_percentage: float
    inferred_type: str
    expected_type: Optional[str]
    type_consistent: bool
    type_consistency_percentage: float
    numeric_stats: Optional[NumericStats]
    outlier_info: Optional[OutlierInfo]


class IssuesSummary(BaseModel):
    """Summary of issues by category"""
    missing_values: int
    invalid_values: int
    outliers: int
    type_inconsistencies: int


class DatasetMetrics(BaseModel):
    """Overall dataset metrics"""
    total_rows: int
    total_columns: int
    total_cells: int


class AdvancedQualityReport(BaseModel):
    """Comprehensive advanced quality report"""
    dataset_metrics: DatasetMetrics
    quality_score: float
    issues_summary: IssuesSummary
    column_quality: List[ColumnQualityReport]
    recommendations: List[str]


# Data Profiling Schemas

class HistogramBin(BaseModel):
    """Histogram bin data"""
    label: str
    midpoint: float
    count: int
    lower: float
    upper: float


class HistogramData(BaseModel):
    """Histogram distribution data"""
    bins: List[HistogramBin]
    total_values: int
    min: Optional[float]
    max: Optional[float]


class CategoryFrequency(BaseModel):
    """Category frequency data"""
    value: str
    count: int
    percentage: float


class OutlierData(BaseModel):
    """Outlier detection data for visualization"""
    has_outliers: bool
    outlier_count: int
    outlier_percentage: float
    lower_bound: Optional[float]
    upper_bound: Optional[float]
    outliers: List[float]
    inliers_count: int
    q1: Optional[float]
    q3: Optional[float]
    iqr: Optional[float]


class ColumnStatistics(BaseModel):
    """Statistical measures for numeric columns"""
    min: float
    max: float
    mean: float
    median: float
    std: float


class MissingValueSummary(BaseModel):
    """Missing value information per column"""
    column_name: str
    null_count: int
    empty_count: int
    total_missing: int
    missing_percentage: float
    present_count: int
    present_percentage: float


class ColumnProfile(BaseModel):
    """Complete profile for a single column"""
    column_name: str
    data_type: str
    is_numeric: bool
    total_values: int
    unique_count: int
    null_count: int
    statistics: Optional[ColumnStatistics] = None
    histogram: Optional[HistogramData] = None
    outliers: Optional[OutlierData] = None
    value_counts: Optional[List[CategoryFrequency]] = None


class DatasetInfo(BaseModel):
    """Dataset-level information"""
    total_rows: int
    total_columns: int
    memory_usage_mb: Optional[float] = None


class ProfilingReport(BaseModel):
    """Complete data profiling report"""
    success: bool
    error: Optional[str] = None
    dataset_info: DatasetInfo
    missing_summary: Optional[List[MissingValueSummary]] = None
    column_profiles: Optional[List[ColumnProfile]] = None
    numeric_columns: Optional[List[str]] = None
    categorical_columns: Optional[List[str]] = None
    total_missing_values: Optional[int] = None
    total_outliers: Optional[int] = None
