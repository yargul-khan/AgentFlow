from pathlib import Path

import pandas as pd


class CSVTool:
    """Tools for inspecting and analyzing CSV files."""

    def __init__(self, sandbox: str = "sandbox/files"):
        self.sandbox = Path(sandbox).resolve()

    def _safe_path(self, path: str) -> Path:
        target = (self.sandbox / path).resolve()

        if self.sandbox not in target.parents:
            raise ValueError("Access outside the sandbox is not allowed.")

        if target.suffix.lower() != ".csv":
            raise ValueError("Only CSV files are supported.")

        return target

    def read_csv(self, path: str) -> str:
        """Return basic information about a CSV file."""

        file_path = self._safe_path(path)
        dataframe = pd.read_csv(file_path)

        return (
            f"Rows: {len(dataframe)}\n"
            f"Columns: {list(dataframe.columns)}\n"
            f"Missing values:\n{dataframe.isnull().sum().to_string()}"
        )

    def analyze_csv(self, path: str) -> str:
        """Look for basic statistical anomalies."""

        file_path = self._safe_path(path)
        dataframe = pd.read_csv(file_path)

        numeric_columns = dataframe.select_dtypes(
            include="number"
        ).columns

        findings = []

        for column in numeric_columns:
            mean = dataframe[column].mean()
            std = dataframe[column].std()

            if std == 0 or pd.isna(std):
                continue

            anomalies = dataframe[
                (dataframe[column] > mean + 3 * std)
                | (dataframe[column] < mean - 3 * std)
            ]

            if not anomalies.empty:
                findings.append(
                    f"{column}: {len(anomalies)} potential anomalies"
                )

        if not findings:
            return "No obvious statistical anomalies were detected."

        return "\n".join(findings)
