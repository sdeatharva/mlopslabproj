import pandas as pd

def check_spelling_variants(train_df: pd.DataFrame, later_df: pd.DataFrame) -> dict:
    """Compare string column categories between train (dirty) and later (clean)."""
    cat_cols = ["boat", "harbour"]
    
    for col in cat_cols:
        train_levels = train_df[col].dropna().unique()
        clean_levels = later_df[col].dropna().unique()
        
        # If train has more variations than the clean later dataset
        if len(train_levels) > len(clean_levels):
            return {
                "present": True,
                "column": col,
                "true_levels": int(len(clean_levels))
            }
            
    return {"present": False, "column": None, "true_levels": None}

def run_checks():
    train_df = pd.read_csv("data/raw/train.csv")
    later_df = pd.read_csv("data/raw/later.csv")
    print("=== CHECK 7: SPELLING VARIANTS ===")
    res = check_spelling_variants(train_df, later_df)
    print(res)

if __name__ == "__main__":
    run_checks()
