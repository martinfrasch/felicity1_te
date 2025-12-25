"""
Data loading utilities for entropy rate and outcome data.

The entropy rate and SampEn files have 11 columns:
- Column 0: subject_id (format: "row_number→patient_code")
- Columns 1-10: Feature estimates (AUC in [0.5-2.5]s interval)
"""

import pandas as pd
import numpy as np
from pathlib import Path


# Column names for entropy rate and SampEn files
FEATURE_COLUMNS = [
    'patient_code',
    'fetus_full',
    'mother_full',
    'fetus_fHR_accel',
    'mother_fHR_accel',
    'fetus_fHR_decel',
    'mother_fHR_decel',
    'fetus_mHR_accel',
    'mother_mHR_accel',
    'fetus_mHR_decel',
    'mother_mHR_decel',
]


def parse_subject_id(subject_id) -> int:
    """
    Parse subject ID to integer.
    """
    return int(subject_id)


def load_feature_file(filepath: Path, prefix: str) -> pd.DataFrame:
    """
    Load entropy rate or SampEn file.

    Args:
        filepath: Path to the data file
        prefix: Prefix for column names (e.g., 'entropy_rate', 'sampen')

    Returns:
        DataFrame with parsed subject IDs and renamed columns
    """
    df = pd.read_csv(
        filepath,
        sep=r'\s+',
        header=None,
        names=FEATURE_COLUMNS,
        na_values=['nan', 'NaN', 'NA']
    )

    # Ensure patient_code is integer
    df['patient_code'] = df['patient_code'].astype(int)

    # Rename feature columns with prefix (skip patient_code)
    rename_map = {
        col: f"{prefix}_{col}"
        for col in FEATURE_COLUMNS[1:]
    }
    df = df.rename(columns=rename_map)

    return df


def load_entropy_rate(data_dir: Path) -> pd.DataFrame:
    """Load entropy rate data."""
    filepath = data_dir / 'entropy_rate.txt'
    return load_feature_file(filepath, 'entropy_rate')


def load_sampen(data_dir: Path) -> pd.DataFrame:
    """Load sample entropy data."""
    filepath = data_dir / 'SampEn.txt'
    return load_feature_file(filepath, 'sampen')


def load_te_files(data_dir: Path) -> pd.DataFrame:
    """
    Load Transfer Entropy files.

    Four files with columns:
    - subject_id
    - sex (1=male, 0=female)
    - stress (1=stressed, 0=non-stressed)
    - net TE all points
    - net TE accelerations
    - net TE decelerations
    """
    te_files = {
        'max_TE_fHR': 'max_TE_fHR_conditioning.csv',
        'max_TE_mHR': 'max_TE_mHR_conditioning.csv',
        'mean_TE_fHR': 'mean_TE_fHR_conditioning.csv',
        'mean_TE_mHR': 'mean_TE_mHR_conditioning.csv',
    }

    te_columns = ['patient_code', 'sex', 'stress', 'all', 'accel', 'decel']

    dfs = []
    for prefix, filename in te_files.items():
        filepath = data_dir / filename
        if not filepath.exists():
            continue

        df = pd.read_csv(
            filepath,
            sep=r'\s+',
            header=None,
            names=te_columns,
            na_values=['nan', 'NaN', 'NA']
        )

        # Rename TE columns with prefix
        rename_map = {
            'all': f'{prefix}_all',
            'accel': f'{prefix}_accel',
            'decel': f'{prefix}_decel',
        }
        df = df.rename(columns=rename_map)

        # Keep only patient_code and TE columns for merging (sex/stress from first file only)
        if len(dfs) == 0:
            # First file: keep sex and stress
            df = df[['patient_code', 'sex', 'stress'] + list(rename_map.values())]
        else:
            # Subsequent files: only keep TE columns
            df = df[['patient_code'] + list(rename_map.values())]

        dfs.append(df)

    if not dfs:
        return pd.DataFrame()

    # Merge all TE dataframes
    result = dfs[0]
    for df in dfs[1:]:
        result = pd.merge(result, df, on='patient_code', how='outer')

    return result


def load_outcomes(data_dir: Path) -> pd.DataFrame:
    """
    Load outcome data from Excel file.

    Returns:
        DataFrame with patient_code as numeric ID
    """
    filepath = data_dir / '210716 EXCEL FILE FOR BAYLEY-STAN.xlsx'
    df = pd.read_excel(filepath)

    # Find the patient code column (usually first column)
    patient_col = df.columns[0]

    # Extract numeric part from "FS-XXX" format
    df['patient_code'] = df[patient_col].astype(str).str.extract(r'(\d+)')[0]
    df['patient_code'] = pd.to_numeric(df['patient_code'], errors='coerce')
    df = df.dropna(subset=['patient_code'])
    df['patient_code'] = df['patient_code'].astype(int)

    # Drop original column if different
    if patient_col != 'patient_code':
        df = df.drop(columns=[patient_col])

    return df


def merge_all_data(data_dir: Path) -> pd.DataFrame:
    """
    Load and merge all data sources.

    Returns:
        Merged DataFrame with entropy rate, SampEn, TE, and outcome features
    """
    # Load all datasets
    entropy_rate = load_entropy_rate(data_dir)
    sampen = load_sampen(data_dir)
    te_data = load_te_files(data_dir)
    outcomes = load_outcomes(data_dir)

    # Merge entropy rate and SampEn
    features = pd.merge(
        entropy_rate,
        sampen,
        on='patient_code',
        how='outer'
    )

    # Merge with TE data
    if not te_data.empty:
        features = pd.merge(
            features,
            te_data,
            on='patient_code',
            how='outer'
        )

    # Merge with outcomes
    merged = pd.merge(
        features,
        outcomes,
        on='patient_code',
        how='inner'
    )

    return merged


def get_te_feature_names() -> list:
    """Get list of TE feature column names."""
    prefixes = ['max_TE_fHR', 'max_TE_mHR', 'mean_TE_fHR', 'mean_TE_mHR']
    suffixes = ['all', 'accel', 'decel']
    return [f'{p}_{s}' for p in prefixes for s in suffixes]


def get_feature_names(prefix: str = None, include_te: bool = True) -> list:
    """
    Get list of feature column names.

    Args:
        prefix: Optional filter for specific feature type ('entropy_rate', 'sampen', or 'te')
        include_te: Whether to include TE features (default True)

    Returns:
        List of feature column names
    """
    base_features = FEATURE_COLUMNS[1:]  # Exclude patient_code

    if prefix == 'te':
        return get_te_feature_names()
    elif prefix:
        return [f"{prefix}_{f}" for f in base_features]

    # Return all features
    features = (
        [f"entropy_rate_{f}" for f in base_features] +
        [f"sampen_{f}" for f in base_features]
    )

    if include_te:
        features += get_te_feature_names()

    return features


if __name__ == '__main__':
    # Test loading
    data_dir = Path(__file__).parent.parent

    print("Loading entropy rate...")
    entropy_rate = load_entropy_rate(data_dir)
    print(f"  Shape: {entropy_rate.shape}")
    print(f"  Columns: {entropy_rate.columns.tolist()}")
    print(f"  Patient codes: {entropy_rate['patient_code'].head(10).tolist()}")

    print("\nLoading SampEn...")
    sampen = load_sampen(data_dir)
    print(f"  Shape: {sampen.shape}")

    print("\nLoading outcomes...")
    outcomes = load_outcomes(data_dir)
    print(f"  Shape: {outcomes.shape}")
    print(f"  Columns: {outcomes.columns.tolist()[:10]}...")

    print("\nMerging all data...")
    merged = merge_all_data(data_dir)
    print(f"  Shape: {merged.shape}")
    print(f"  Columns: {len(merged.columns)}")
