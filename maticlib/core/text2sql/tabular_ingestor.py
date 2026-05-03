import os
from typing import Optional
from maticlib.exceptions import MissingDependencyError, TabularIngestionError


class TabularIngestor:
    def __init__(self, connection_string: str = "sqlite:///maticlib_data.db"):
        self.connection_string = connection_string
        try:
            from sqlalchemy import create_engine

            self.engine = create_engine(self.connection_string)
        except ImportError as e:
            raise MissingDependencyError(
                "sqlalchemy is required for TabularIngestor. Install it with: pip install maticlib[tabular]"
            ) from e

    def ingest_file(
        self, source: str, table_name: Optional[str] = None, if_exists: str = "replace"
    ):
        """
        Ingest a CSV, Excel, or Parquet file into the database.
        if_exists can be 'fail', 'replace', or 'append'.
        """
        try:
            import pandas as pd
        except ImportError as e:
            raise MissingDependencyError(
                "pandas is required for TabularIngestor. Install it with: pip install maticlib[tabular]"
            ) from e

        if not os.path.exists(source):
            raise TabularIngestionError(f"File not found: {source}")

        if not table_name:
            # Default table name from filename
            base = os.path.basename(source)
            table_name = (
                os.path.splitext(base)[0].lower().replace(" ", "_").replace("-", "_")
            )

        ext = os.path.splitext(source)[1].lower()

        try:
            if ext == ".csv":
                df = pd.read_csv(source)
            elif ext in [".xls", ".xlsx"]:
                try:
                    import openpyxl  # noqa
                except ImportError:
                    raise MissingDependencyError(
                        "openpyxl is required for Excel files. pip install openpyxl"
                    )
                df = pd.read_excel(source)
            elif ext == ".parquet":
                try:
                    import pyarrow  # noqa
                except ImportError:
                    raise MissingDependencyError(
                        "pyarrow is required for Parquet files. pip install pyarrow"
                    )
                df = pd.read_parquet(source)
            else:
                raise TabularIngestionError(f"Unsupported file format: {ext}")

            df.to_sql(
                name=table_name, con=self.engine, if_exists=if_exists, index=False
            )
            return table_name
        except Exception as e:
            if isinstance(e, (MissingDependencyError, TabularIngestionError)):
                raise
            raise TabularIngestionError(f"Failed to ingest file {source}: {e}")
