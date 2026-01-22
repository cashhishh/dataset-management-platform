"""
Advanced data quality analysis service.
Provides column-level quality checks including outlier detection,
type consistency validation, and invalid value detection.
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Any, Optional
import logging

logger = logging.getLogger(__name__)


class AdvancedQualityAnalyzer:
    """Advanced data quality analysis with column-level insights"""

    @staticmethod
    def detect_outliers_iqr(series: pd.Series, multiplier: float = 1.5) -> Dict[str, Any]:
        """
        Detect outliers using Interquartile Range (IQR) method.
        
        Args:
            series: Pandas series to analyze
            multiplier: IQR multiplier (default 1.5)
            
        Returns:
            Dict with outlier statistics
        """
        try:
            # Remove non-numeric values
            numeric_series = pd.to_numeric(series, errors='coerce').dropna()
            
            if len(numeric_series) == 0:
                return {
                    "outlier_count": 0,
                    "outlier_percentage": 0.0,
                    "lower_bound": None,
                    "upper_bound": None,
                    "outliers": []
                }
            
            Q1 = numeric_series.quantile(0.25)
            Q3 = numeric_series.quantile(0.75)
            IQR = Q3 - Q1
            
            lower_bound = Q1 - (multiplier * IQR)
            upper_bound = Q3 + (multiplier * IQR)
            
            outliers = numeric_series[(numeric_series < lower_bound) | (numeric_series > upper_bound)]
            outlier_count = len(outliers)
            outlier_percentage = (outlier_count / len(numeric_series)) * 100
            
            return {
                "outlier_count": int(outlier_count),
                "outlier_percentage": round(outlier_percentage, 2),
                "lower_bound": float(lower_bound),
                "upper_bound": float(upper_bound),
                "outliers": outliers.head(10).tolist()  # Return max 10 examples
            }
            
        except Exception as e:
            logger.warning(f"Outlier detection failed: {e}")
            return {
                "outlier_count": 0,
                "outlier_percentage": 0.0,
                "lower_bound": None,
                "upper_bound": None,
                "outliers": []
            }

    @staticmethod
    def analyze_column_quality(
        df: pd.DataFrame,
        column_name: str,
        expected_type: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Analyze quality metrics for a single column.
        
        Args:
            df: DataFrame containing the column
            column_name: Name of the column to analyze
            expected_type: Expected data type (optional)
            
        Returns:
            Dict with column quality metrics
        """
        try:
            series = df[column_name]
            total_count = len(series)
            
            # Basic metrics
            null_count = int(series.isnull().sum())
            empty_string_count = int((series == "").sum()) if series.dtype == 'object' else 0
            
            # Inferred type
            inferred_type = str(series.dtype)
            
            # Type consistency
            type_consistent = True
            if expected_type and expected_type != inferred_type:
                type_consistent = False
            
            # Numeric analysis
            numeric_stats = None
            outlier_info = None
            
            if pd.api.types.is_numeric_dtype(series):
                valid_numeric = series.dropna()
                if len(valid_numeric) > 0:
                    numeric_stats = {
                        "min": float(valid_numeric.min()),
                        "max": float(valid_numeric.max()),
                        "mean": float(valid_numeric.mean()),
                        "median": float(valid_numeric.median()),
                        "std": float(valid_numeric.std()) if len(valid_numeric) > 1 else 0.0
                    }
                    
                    # Outlier detection
                    outlier_info = AdvancedQualityAnalyzer.detect_outliers_iqr(series)
            
            # Invalid values (values that can't be parsed)
            invalid_count = 0
            if series.dtype == 'object':
                # Try to convert to numeric and count failures
                try:
                    pd.to_numeric(series, errors='coerce')
                    invalid_count = int(series.notna().sum() - pd.to_numeric(series, errors='coerce').notna().sum())
                except:
                    invalid_count = 0
            
            # Unique values
            unique_count = int(series.nunique())
            unique_percentage = (unique_count / total_count * 100) if total_count > 0 else 0.0
            
            # Completeness
            completeness = ((total_count - null_count - empty_string_count) / total_count * 100) if total_count > 0 else 0.0
            
            # Calculate percentages
            null_percentage = (null_count / total_count * 100) if total_count > 0 else 0.0
            empty_percentage = (empty_string_count / total_count * 100) if total_count > 0 else 0.0
            type_consistency_percentage = 100.0 if type_consistent else 0.0
            
            return {
                "column_name": column_name,
                "total_values": total_count,
                "null_count": null_count,
                "null_percentage": round(null_percentage, 2),
                "empty_string_count": empty_string_count,
                "empty_percentage": round(empty_percentage, 2),
                "invalid_count": invalid_count,
                "unique_count": unique_count,
                "unique_percentage": round(unique_percentage, 2),
                "completeness_percentage": round(completeness, 2),
                "inferred_type": inferred_type,
                "expected_type": expected_type,
                "type_consistent": type_consistent,
                "type_consistency_percentage": round(type_consistency_percentage, 2),
                "numeric_stats": numeric_stats,
                "outlier_info": outlier_info
            }
            
        except Exception as e:
            logger.error(f"Column quality analysis failed for {column_name}: {e}")
            return {
                "column_name": column_name,
                "error": str(e),
                "total_values": 0,
                "null_count": 0,
                "completeness_percentage": 0.0
            }

    @staticmethod
    def generate_advanced_quality_report(
        file_path: str,
        column_metadata: Optional[List[Dict]] = None
    ) -> Dict[str, Any]:
        """
        Generate comprehensive quality report for a dataset.
        
        Args:
            file_path: Path to CSV file
            column_metadata: Optional list of column metadata with expected types
            
        Returns:
            Dict with comprehensive quality report
        """
        try:
            logger.info(f"Generating advanced quality report for: {file_path}")
            
            # Load dataset
            df = pd.read_csv(file_path, encoding="utf-8", engine="python")
            
            total_rows = len(df)
            total_columns = len(df.columns)
            
            # Column-level analysis
            column_reports = []
            expected_types = {}
            
            if column_metadata:
                expected_types = {
                    col["column_name"]: col.get("data_type", col.get("column_type"))
                    for col in column_metadata
                }
            
            for column in df.columns:
                expected_type = expected_types.get(column)
                col_report = AdvancedQualityAnalyzer.analyze_column_quality(
                    df, column, expected_type
                )
                column_reports.append(col_report)
            
            # Aggregate statistics
            total_null_count = sum(col["null_count"] for col in column_reports)
            total_empty_strings = sum(col.get("empty_string_count", 0) for col in column_reports)
            total_invalid_values = sum(col.get("invalid_count", 0) for col in column_reports)
            total_outliers = sum(
                col.get("outlier_info", {}).get("outlier_count", 0)
                for col in column_reports
                if col.get("outlier_info")
            )
            
            # Issue categorization
            issues_by_category = {
                "missing_values": total_null_count + total_empty_strings,
                "invalid_values": total_invalid_values,
                "outliers": total_outliers,
                "type_inconsistencies": sum(
                    1 for col in column_reports
                    if not col.get("type_consistent", True)
                )
            }
            
            # Overall quality score (0-100)
            total_cells = total_rows * total_columns
            problematic_cells = (
                total_null_count +
                total_empty_strings +
                total_invalid_values
            )
            
            quality_score = (
                ((total_cells - problematic_cells) / total_cells * 100)
                if total_cells > 0 else 100.0
            )
            
            return {
                "dataset_metrics": {
                    "total_rows": total_rows,
                    "total_columns": total_columns,
                    "total_cells": total_cells
                },
                "quality_score": round(quality_score, 2),
                "issues_summary": issues_by_category,
                "column_quality": column_reports,
                "recommendations": AdvancedQualityAnalyzer._generate_recommendations(
                    column_reports, issues_by_category
                )
            }
            
        except Exception as e:
            logger.error(f"Advanced quality report generation failed: {e}", exc_info=True)
            raise ValueError(f"Failed to generate quality report: {str(e)}")

    @staticmethod
    def _generate_recommendations(
        column_reports: List[Dict],
        issues_summary: Dict[str, int]
    ) -> List[str]:
        """Generate actionable recommendations based on quality issues"""
        recommendations = []
        
        if issues_summary["missing_values"] > 0:
            recommendations.append(
                f"Found {issues_summary['missing_values']} missing values. "
                "Consider imputation or removing incomplete rows."
            )
        
        if issues_summary["outliers"] > 0:
            recommendations.append(
                f"Detected {issues_summary['outliers']} outliers across numeric columns. "
                "Review and validate extreme values."
            )
        
        if issues_summary["type_inconsistencies"] > 0:
            recommendations.append(
                f"Found {issues_summary['type_inconsistencies']} columns with type inconsistencies. "
                "Verify data types match expectations."
            )
        
        if issues_summary["invalid_values"] > 0:
            recommendations.append(
                f"Found {issues_summary['invalid_values']} invalid values. "
                "Clean or standardize data format."
            )
        
        # Check for low completeness columns
        low_completeness_cols = [
            col["column_name"]
            for col in column_reports
            if col.get("completeness_percentage", 100) < 50
        ]
        
        if low_completeness_cols:
            recommendations.append(
                f"Columns with <50% completeness: {', '.join(low_completeness_cols[:3])}. "
                "Consider removing or imputing these columns."
            )
        
        if not recommendations:
            recommendations.append("Dataset quality is good. No major issues detected.")
        
        return recommendations
