"""
Data profiling service for generating visualization-ready statistics.
Provides distribution data, frequency counts, and missing value analysis.
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Any, Optional
import logging

logger = logging.getLogger(__name__)


class DataProfiler:
    """Generate visualization-ready profiling statistics for datasets"""

    @staticmethod
    def generate_histogram_bins(series: pd.Series, num_bins: int = 20) -> Dict[str, Any]:
        """
        Generate histogram bin data for numeric columns.
        
        Args:
            series: Pandas series to analyze
            num_bins: Number of histogram bins
            
        Returns:
            Dict with bin edges and counts
        """
        try:
            numeric_series = pd.to_numeric(series, errors='coerce').dropna()
            
            if len(numeric_series) == 0:
                return {
                    "bins": [],
                    "counts": [],
                    "min": None,
                    "max": None
                }
            
            counts, bin_edges = np.histogram(numeric_series, bins=num_bins)
            
            # Create bin labels (midpoints for visualization)
            bins = []
            for i in range(len(bin_edges) - 1):
                midpoint = (bin_edges[i] + bin_edges[i + 1]) / 2
                bins.append({
                    "label": f"{bin_edges[i]:.2f}-{bin_edges[i+1]:.2f}",
                    "midpoint": round(float(midpoint), 2),
                    "count": int(counts[i]),
                    "lower": round(float(bin_edges[i]), 2),
                    "upper": round(float(bin_edges[i + 1]), 2)
                })
            
            return {
                "bins": bins,
                "total_values": int(len(numeric_series)),
                "min": round(float(numeric_series.min()), 2),
                "max": round(float(numeric_series.max()), 2)
            }
            
        except Exception as e:
            logger.error(f"Histogram generation failed: {e}")
            return {
                "bins": [],
                "counts": [],
                "min": None,
                "max": None
            }

    @staticmethod
    def get_categorical_frequencies(
        series: pd.Series, 
        top_n: int = 15,
        min_frequency: int = 1
    ) -> List[Dict[str, Any]]:
        """
        Get value frequency counts for categorical columns.
        
        Args:
            series: Pandas series to analyze
            top_n: Maximum number of categories to return
            min_frequency: Minimum frequency to include
            
        Returns:
            List of dicts with value and count
        """
        try:
            # Remove null values
            valid_series = series.dropna()
            
            if len(valid_series) == 0:
                return []
            
            # Get value counts
            value_counts = valid_series.value_counts()
            
            # Filter by minimum frequency
            value_counts = value_counts[value_counts >= min_frequency]
            
            # Limit to top N
            value_counts = value_counts.head(top_n)
            
            # Convert to list of dicts
            frequencies = [
                {
                    "value": str(value),
                    "count": int(count),
                    "percentage": round((count / len(valid_series)) * 100, 2)
                }
                for value, count in value_counts.items()
            ]
            
            # Add "Other" category if there are more values
            if len(series.dropna().unique()) > top_n:
                other_count = len(valid_series) - sum(f["count"] for f in frequencies)
                if other_count > 0:
                    frequencies.append({
                        "value": "Other",
                        "count": other_count,
                        "percentage": round((other_count / len(valid_series)) * 100, 2)
                    })
            
            return frequencies
            
        except Exception as e:
            logger.error(f"Categorical frequency calculation failed: {e}")
            return []

    @staticmethod
    def get_missing_values_summary(df: pd.DataFrame) -> List[Dict[str, Any]]:
        """
        Get missing value counts for all columns.
        
        Args:
            df: DataFrame to analyze
            
        Returns:
            List of dicts with column name, missing count, and percentage
        """
        try:
            total_rows = len(df)
            missing_summary = []
            
            for column in df.columns:
                null_count = int(df[column].isnull().sum())
                empty_count = 0
                
                # Count empty strings for object columns
                if df[column].dtype == 'object':
                    empty_count = int((df[column] == "").sum())
                
                total_missing = null_count + empty_count
                missing_percentage = (total_missing / total_rows * 100) if total_rows > 0 else 0
                
                missing_summary.append({
                    "column_name": column,
                    "null_count": null_count,
                    "empty_count": empty_count,
                    "total_missing": total_missing,
                    "missing_percentage": round(missing_percentage, 2),
                    "present_count": total_rows - total_missing,
                    "present_percentage": round(100 - missing_percentage, 2)
                })
            
            return missing_summary
            
        except Exception as e:
            logger.error(f"Missing values summary failed: {e}")
            return []

    @staticmethod
    def detect_outliers_for_visualization(
        series: pd.Series, 
        multiplier: float = 1.5
    ) -> Dict[str, Any]:
        """
        Detect outliers using IQR method for visualization.
        
        Args:
            series: Pandas series to analyze
            multiplier: IQR multiplier
            
        Returns:
            Dict with outlier information and bounds
        """
        try:
            numeric_series = pd.to_numeric(series, errors='coerce').dropna()
            
            if len(numeric_series) == 0:
                return {
                    "has_outliers": False,
                    "outlier_count": 0,
                    "lower_bound": None,
                    "upper_bound": None,
                    "outliers": [],
                    "inliers_count": 0
                }
            
            Q1 = numeric_series.quantile(0.25)
            Q3 = numeric_series.quantile(0.75)
            IQR = Q3 - Q1
            
            lower_bound = Q1 - (multiplier * IQR)
            upper_bound = Q3 + (multiplier * IQR)
            
            outlier_mask = (numeric_series < lower_bound) | (numeric_series > upper_bound)
            outliers = numeric_series[outlier_mask]
            
            # Limit outlier values to prevent huge payloads
            outlier_values = [round(float(x), 2) for x in outliers.head(50)]
            
            return {
                "has_outliers": len(outliers) > 0,
                "outlier_count": int(len(outliers)),
                "outlier_percentage": round((len(outliers) / len(numeric_series)) * 100, 2),
                "lower_bound": round(float(lower_bound), 2),
                "upper_bound": round(float(upper_bound), 2),
                "outliers": outlier_values,
                "inliers_count": int(len(numeric_series) - len(outliers)),
                "q1": round(float(Q1), 2),
                "q3": round(float(Q3), 2),
                "iqr": round(float(IQR), 2)
            }
            
        except Exception as e:
            logger.error(f"Outlier detection failed: {e}")
            return {
                "has_outliers": False,
                "outlier_count": 0,
                "lower_bound": None,
                "upper_bound": None,
                "outliers": [],
                "inliers_count": 0
            }

    @staticmethod
    def profile_column(
        df: pd.DataFrame, 
        column_name: str,
        is_numeric: bool = None
    ) -> Dict[str, Any]:
        """
        Generate complete profile for a single column.
        
        Args:
            df: DataFrame containing the column
            column_name: Name of column to profile
            is_numeric: Whether column is numeric (auto-detect if None)
            
        Returns:
            Dict with complete column profile
        """
        try:
            series = df[column_name]
            
            # Auto-detect if numeric
            if is_numeric is None:
                is_numeric = pd.api.types.is_numeric_dtype(series)
            
            profile = {
                "column_name": column_name,
                "data_type": str(series.dtype),
                "is_numeric": is_numeric,
                "total_values": int(len(series)),
                "unique_count": int(series.nunique()),
                "null_count": int(series.isnull().sum())
            }
            
            # Add numeric-specific profiling
            if is_numeric:
                numeric_series = pd.to_numeric(series, errors='coerce').dropna()
                
                if len(numeric_series) > 0:
                    profile["statistics"] = {
                        "min": round(float(numeric_series.min()), 2),
                        "max": round(float(numeric_series.max()), 2),
                        "mean": round(float(numeric_series.mean()), 2),
                        "median": round(float(numeric_series.median()), 2),
                        "std": round(float(numeric_series.std()), 2) if len(numeric_series) > 1 else 0.0
                    }
                    
                    # Histogram data
                    profile["histogram"] = DataProfiler.generate_histogram_bins(series)
                    
                    # Outlier information
                    profile["outliers"] = DataProfiler.detect_outliers_for_visualization(series)
                else:
                    profile["statistics"] = None
                    profile["histogram"] = None
                    profile["outliers"] = None
            
            # Add categorical-specific profiling
            else:
                profile["value_counts"] = DataProfiler.get_categorical_frequencies(series)
            
            return profile
            
        except Exception as e:
            logger.error(f"Column profiling failed for {column_name}: {e}")
            return {
                "column_name": column_name,
                "error": str(e),
                "data_type": "unknown",
                "is_numeric": False,
                "total_values": 0
            }

    @staticmethod
    def generate_full_profile(
        file_path: str,
        max_columns: int = 50
    ) -> Dict[str, Any]:
        """
        Generate complete profiling data for entire dataset.
        
        Args:
            file_path: Path to CSV file
            max_columns: Maximum columns to profile (safety limit)
            
        Returns:
            Dict with complete dataset profile
        """
        try:
            # Load dataset
            df = pd.read_csv(file_path)
            
            if df.empty:
                return {
                    "success": False,
                    "error": "Dataset is empty",
                    "dataset_info": {
                        "total_rows": 0,
                        "total_columns": 0
                    }
                }
            
            # Limit columns to prevent performance issues
            if len(df.columns) > max_columns:
                logger.warning(f"Dataset has {len(df.columns)} columns, limiting to {max_columns}")
                df = df.iloc[:, :max_columns]
            
            # Dataset-level info
            dataset_info = {
                "total_rows": int(len(df)),
                "total_columns": int(len(df.columns)),
                "memory_usage_mb": round(df.memory_usage(deep=True).sum() / (1024 * 1024), 2)
            }
            
            # Missing values summary
            missing_summary = DataProfiler.get_missing_values_summary(df)
            
            # Profile each column
            column_profiles = []
            numeric_columns = []
            categorical_columns = []
            
            for column in df.columns:
                is_numeric = pd.api.types.is_numeric_dtype(df[column])
                
                profile = DataProfiler.profile_column(df, column, is_numeric)
                column_profiles.append(profile)
                
                if is_numeric:
                    numeric_columns.append(column)
                else:
                    categorical_columns.append(column)
            
            return {
                "success": True,
                "dataset_info": dataset_info,
                "missing_summary": missing_summary,
                "column_profiles": column_profiles,
                "numeric_columns": numeric_columns,
                "categorical_columns": categorical_columns,
                "total_missing_values": sum(m["total_missing"] for m in missing_summary),
                "total_outliers": sum(
                    (p.get("outliers") or {}).get("outlier_count", 0) 
                    for p in column_profiles 
                    if p.get("is_numeric", False)
                )
            }
            
        except FileNotFoundError:
            logger.error(f"File not found: {file_path}")
            return {
                "success": False,
                "error": "Dataset file not found",
                "dataset_info": {
                    "total_rows": 0,
                    "total_columns": 0
                }
            }
        except Exception as e:
            logger.error(f"Profiling failed: {e}", exc_info=True)
            return {
                "success": False,
                "error": f"Profiling failed: {str(e)}",
                "dataset_info": {
                    "total_rows": 0,
                    "total_columns": 0
                }
            }
