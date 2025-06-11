import pandas as pd

def print_with_colors(msg: str, color: str, end: str = "\n") -> None:
    """
    Prints a message in the specified color using ANSI escape codes.
    :param msg: The message to print.
    :param color: The color to print the message in. Supported colors are:
                  'black', 'red', 'green', 'yellow', 'blue', 'magenta', 'cyan', 'white'.
    """
    colors = {
        "black": "\033[30m",
        "red": "\033[31m",
        "green": "\033[32m",
        "yellow": "\033[33m",
        "blue": "\033[34m",
        "magenta": "\033[35m",
        "cyan": "\033[36m",
        "white": "\033[37m",
    }
    reset_color = "\033[0m"

    c_code = colors.get(color.lower())

    if c_code:
        print(f"{c_code}{msg}{reset_color}", end=end)
    else:
        print(f"(Warning: Color '{color}' not found. printing with default color.)")
        print(msg, end=end)


def is_int(val):
    """
    Verify if a given value is integer, ignoring NaNs.
    """
    try:
        # Try to convert to integer, ignoring NaN
        if pd.isnull(val):
            return False
        int(val)
        return True
    except (ValueError, TypeError):
        return False

import pandas as pd
import numpy as np

def process_num_like_cols(df: pd.DataFrame, threshold: float = 0.5) -> pd.DataFrame:
    """
    Analyzes 'object' or 'category' columns and converts them to numeric type
    if the majority of their values are "number-like".

        Values that cannot be converted to number in the selected column
    are transformed into NaN.

        Args:
    df (pd.DataFrame): The DataFrame to be cleared.
    threshold (float): The proportion of numeric values (between 0.0 and 1.0)
    required for a column to be considered "mostly
    numeric". The default is 0.5 (50%).

        Returns:
    pd.DataFrame: The DataFrame with the columns cleaned up. The modification is
    made to the original DataFrame (in-place) to save memory.
    """

    converted_cols = []
    
    cols_to_verify = df.columns

    for col in cols_to_verify:
        nan_free_col = df[col].dropna()

        if nan_free_col.empty:
            print_with_colors(f"  - Feature '{col}' only had NaN values, dropping...", "red", end="\n\n")
            df = df.drop(columns=[col])
            continue

        nums_vals = pd.to_numeric(nan_free_col.astype(str), errors='coerce')

        nums_ratio = nums_vals.notna().sum() / len(nan_free_col)

        if nums_ratio > threshold:
            print_with_colors(f"  - Feature '{col}': {nums_ratio:.2%} of values are numeric. Converting...", "yellow", end="\n\n")
            
            df[col] = pd.to_numeric(df[col].astype(str), errors='coerce')
            converted_cols.append(col)
        else:
             print_with_colors(f"  - Feature '{col}': {nums_ratio:.2%} of values are numeric. Keeping as is.", "yellow", end="\n\n")

    print(f"Features converted to numeric data type: {converted_cols}")
    return df

def print_with_multiple_columns(columns: list, n_cols: int = 5) -> None:
    """
    Prints multiple columns with their corresponding values in a formatted way.
    
    :param columns: List of column names.
    :param n_cols: The amount of columns to be printed in each row.
    """
    n = 0
    max_width = max(len(str(col)) for col in columns)
    for col in columns:
        if n // n_cols == 0:
            print(f"{col:<{max_width + 2}}", end=" ")
            n += 1
        else:
            print(f"{col:<{max_width + 2}}", end="\n")
            n = 0