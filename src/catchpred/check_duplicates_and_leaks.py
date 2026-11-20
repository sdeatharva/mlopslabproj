import pandas as pd
from pathlib import Path

def check_duplicate_rows(df: pd.DataFrame) -> dict:
    """Check for duplicate rows in train.csv."""
    # We ignore record_id if needed, but exact duplicate rows check all columns
    duplicates_count = int(df.duplicated().sum())
    present = duplicates_count > 0
    return {
        "present": present,
        "count": duplicates_count if present else None
    }

def check_leaking_column(train_df: pd.DataFrame, holdout_df: pd.DataFrame) -> dict:
    """Check for columns present in train but missing in holdout (and not target)."""
    train_cols = set(train_df.columns)
    holdout_cols = set(holdout_df.columns)
    
    # Columns in train that are NOT in holdout and NOT the target 'catch_kg'
    potential_leaks = train_cols - holdout_cols - {"catch_kg"}
    
    if potential_leaks:
        leaking_col = list(potential_leaks)[0]
        return {
            "present": True,
            "column": leaking_col
        }
    return {
        "present": False,
        "column": None
    }

def run_checks():
    data_dir = Path("data/raw")
    train_path = data_dir / "train.csv"
    holdout_path = data_dir / "holdout_features.csv"
    
    train_df = pd.read_csv(train_path)
    holdout_df = pd.read_csv(holdout_path)
    
    print("=== CHECK 1: DUPLICATE ROWS ===")
    dup_res = check_duplicate_rows(train_df)
    print(dup_res)
    
    print("\n=== CHECK 2: LEAKING COLUMN ===")
    leak_res = check_leaking_column(train_df, holdout_df)
    print(leak_res)

if __name__ == "__main__":
    run_checks()
