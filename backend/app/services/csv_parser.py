"""
CSV parsing and metadata extraction service.
"""

import pandas as pd
from typing import Dict, List, Any
import logging
import math

logger = logging.getLogger(__name__)


class CSVParser:
    """Parse CSV files and extract metadata"""

    @staticmethod
    def _sanitize_records(records: List[Dict]) -> List[Dict]:
        """
        Convert NaN / inf values to None so JSON serialization never fails.
        """
        sanitized = []
        for row in records:
            clean_row = {}
            for k, v in row.items():
                if isinstance(v, float) and (math.isnan(v) or math.isinf(v)):
                    clean_row[k] = None
                else:
                    clean_row[k] = v
            sanitized.append(clean_row)
        return sanitized

    @staticmethod
    def parse_csv_file(file_path: str) -> Dict[str, Any]:
        logger.info(f"Parsing CSV file: {file_path}")

        try:
            df = pd.read_csv(
                file_path,
                encoding="utf-8",
                engine="python"
            )

            row_count = len(df)
            column_count = len(df.columns)

            logger.info(f"CSV loaded: {row_count} rows × {column_count} columns")

            columns = []
            for idx, col in enumerate(df.columns):
                columns.append({
                    "name": str(col),
                    "type": str(df[col].dtype),
                    "index": idx
                })

            preview = CSVParser._sanitize_records(
                df.head(5).to_dict(orient="records")
            )

            return {
                "df": df,
                "row_count": row_count,
                "column_count": column_count,
                "columns": columns,
                "preview": preview
            }

        except Exception as e:
            logger.error(f"CSV parsing failed: {e}", exc_info=True)
            raise ValueError("Failed to parse CSV file")

    @staticmethod
    def analyze_data_quality(df: pd.DataFrame) -> Dict[str, Any]:
        logger.info("Analyzing data quality...")

        try:
            total_rows = len(df)
            total_columns = len(df.columns)

            duplicate_rows = int(df.duplicated().sum())
            null_counts = {
                str(col): int(df[col].isnull().sum())
                for col in df.columns
            }

            total_cells = total_rows * total_columns
            null_cells = sum(null_counts.values())

            completeness_score = (
                ((total_cells - null_cells) / total_cells) * 100
                if total_cells > 0 else 100.0
            )

            return {
                "total_rows": total_rows,
                "total_columns": total_columns,
                "duplicate_rows": duplicate_rows,
                "null_counts": null_counts,
                "completeness_score": round(completeness_score, 2)
            }

        except Exception as e:
            logger.error(f"Quality analysis failed: {e}", exc_info=True)
            raise ValueError("Failed to analyze data quality")

    @staticmethod
    def get_preview_data(file_path: str, limit: int = 10) -> List[Dict]:
        try:
            df = pd.read_csv(
                file_path,
                nrows=limit,
                encoding="utf-8",
                engine="python"
            )
            records = df.to_dict(orient="records")
            return CSVParser._sanitize_records(records)

        except Exception as e:
            logger.error(f"Preview failed: {e}", exc_info=True)
            raise ValueError("Failed to load preview data")
