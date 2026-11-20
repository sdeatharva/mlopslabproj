import pandas as pd
from pathlib import Path

def check_stuck_sensor(df: pd.DataFrame, min_consecutive_days: int = 7) -> dict:
    """Check if a sensor reported the identical float/int value for consecutive days."""
    df_sorted = df.sort_values("date").reset_index(drop=True)
    numeric_cols = [c for c in df_sorted.select_dtypes(include="number").columns if c not in ["catch_kg"]]
    
    for col in numeric_cols:
        # Group consecutive equal values
        is_same = (df_sorted[col] == df_sorted[col].shift())
        groups = (~is_same).cumsum()
        streak_sizes = df_sorted.groupby(groups).size()
        
        longest_group = streak_sizes.idxmax()
        longest_streak = streak_sizes.max()
        
        # Check date range of the longest streak
        streak_rows = df_sorted[groups == longest_group]
        start_date = streak_rows["date"].iloc[0]
        end_date = streak_rows["date"].iloc[-1]
        
        days_span = (pd.to_datetime(end_date) - pd.to_datetime(start_date)).days
        if days_span >= min_consecutive_days and longest_streak > 10:
            return {
                "present": True,
                "column": col,
                "start_date": str(start_date),
                "end_date": str(end_date)
            }
            
    return {"present": False, "column": None, "start_date": None, "end_date": None}

def run_checks():
    train_df = pd.read_csv("data/raw/train.csv")
    print("=== CHECK 5: STUCK SENSOR ===")
    res = check_stuck_sensor(train_df)
    print(res)

if __name__ == "__main__":
    run_checks()
