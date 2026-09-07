import pandas as pd


def normalize_dataset(df: pd.DataFrame, mapping: dict) -> pd.DataFrame:
    """
    Rename uploaded CSV columns to BusinessPulse standard fields.
    """

    rename_mapping = {
        csv_column: standard_field for standard_field, csv_column in mapping.items()
    }

    normalized_df = df.rename(columns=rename_mapping)

    return normalized_df
