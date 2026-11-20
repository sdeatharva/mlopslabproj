import pandas as pd
import numpy as np

def check_target_typos(df: pd.DataFrame, target_col: str = "catch_kg") -> dict:
    """Check if a small cluster of targets were typed with an extra zero (10x too big)."""
    sorted_targets = df[target_col].dropna().sort_values().values
    
    # Compare 95th percentile with max
    p95 = np.percentile(sorted_targets, 95)
    p99 = np.percentile(sorted_targets, 99)
    
    # Typos with an extra zero sit around ~10x normal max
    typo_candidates = df[df[target_col] >= p95 * 5][target_col]
    count = int(len(typo_candidates))
    
    if count > 0 and count < 25: # small group of outliers
        return {
            "present": True,
            "count": count
        }
    return {
        "present": False,
        "count": None
    }

def run_checks():
    train_df = pd.read_csv("data/raw/train.csv")
    print("=== CHECK 6: TARGET TYPOS ===")
    res = check_target_typos(train_df)
    print(res)

if __name__ == "__main__":
    run_checks()
