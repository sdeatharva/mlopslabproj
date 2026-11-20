import pandas as pd
from pathlib import Path

def check_unit_mixup(df: pd.DataFrame, group_col: str = "harbour") -> dict:
    """Check if one harbour has a numeric column off by an exact factor (e.g. 1000, 100, 10)."""
    numeric_cols = [c for c in df.select_dtypes(include="number").columns if c not in ["catch_kg"]]
    groups = df[group_col].dropna().unique()
    
    candidate_factors = [1000, 100, 60, 12, 10]
    
    for col in numeric_cols:
        medians = df.groupby(group_col)[col].median()
        for g in groups:
            other_medians = [medians[o] for o in groups if o != g and medians[o] > 0]
            if not other_medians:
                continue
            avg_others = sum(other_medians) / len(other_medians)
            if avg_others == 0:
                continue
            ratio = medians[g] / avg_others
            
            for f in candidate_factors:
                if 0.8 * f <= ratio <= 1.2 * f:
                    return {
                        "present": True,
                        "column": col,
                        "group_value": g,
                        "factor": f
                    }
    return {"present": False, "column": None, "group_value": None, "factor": None}

def check_sentinel_value(df: pd.DataFrame) -> dict:
    """Check for impossible typed numbers like -999, -1, 9999 used as placeholders."""
    numeric_cols = [c for c in df.select_dtypes(include="number").columns if c not in ["catch_kg"]]
    common_sentinels = [-999, -1, 999, 9999]
    
    for col in numeric_cols:
        for sentinel in common_sentinels:
            count = int((df[col] == sentinel).sum())
            if count > 0:
                return {
                    "present": True,
                    "column": col,
                    "value": sentinel,
                    "count": count
                }
        # Also check negative values for non-negative physical quantities
        negatives = df[df[col] < 0][col].value_counts()
        if not negatives.empty:
            sentinel_val = negatives.index[0]
            return {
                "present": True,
                "column": col,
                "value": float(sentinel_val) if isinstance(sentinel_val, float) else int(sentinel_val),
                "count": int(negatives.iloc[0])
            }
            
    return {"present": False, "column": None, "value": None, "count": None}

def run_checks():
    train_df = pd.read_csv("data/raw/train.csv")
    
    print("=== CHECK 3: UNIT MIXUP ===")
    unit_res = check_unit_mixup(train_df)
    print(unit_res)
    
    print("\n=== CHECK 4: SENTINEL VALUE ===")
    sentinel_res = check_sentinel_value(train_df)
    print(sentinel_res)

if __name__ == "__main__":
    run_checks()
