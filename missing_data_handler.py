import pandas as pd

# Function to detect missing data
def detect_missing_data(df):
    df['datetime'] = pd.to_datetime(df['timestamp'], unit='ms')
    df = df.set_index('datetime')
    
    # Calculate the expected time difference
    expected_diff = pd.Timedelta('1min')
    
    # Detect where the difference between consecutive rows is not equal to the expected difference
    missing_rows = df[df.index.to_series().diff() > expected_diff]
    
    # Reset index to keep the structure
    df = df.reset_index(drop=True)
    
    if missing_rows.empty:
        print("No missing data detected.")
    else:
        print("Missing data detected at the following rows and times:")
        print(missing_rows[['timestamp']])
    
    return missing_rows

# Function to fill missing data
def fill_missing_data(df):
    df['datetime'] = pd.to_datetime(df['timestamp'], unit='ms')
    df = df.set_index('datetime')
    
    # Resample to fill missing data with 1-minute frequency
    df_filled = df.resample('1T').mean().interpolate()
    
    # Recreate the timestamp column
    df_filled['timestamp'] = df_filled.index.astype(int) // 10**6
    
    # Reset index to get back the original structure
    df_filled = df_filled.reset_index(drop=True)
    
    return df_filled

# Function to find the added rows after filling
def find_added_rows(original_df, filled_df):
    # Convert timestamp to datetime for comparison
    original_df['datetime'] = pd.to_datetime(original_df['timestamp'], unit='ms')
    filled_df['datetime'] = pd.to_datetime(filled_df['timestamp'], unit='ms')
    
    # Set datetime as index for comparison
    original_df = original_df.set_index('datetime')
    filled_df = filled_df.set_index('datetime')
    
    # Find rows that are in filled_df but not in original_df
    added_rows = filled_df.loc[~filled_df.index.isin(original_df.index)]
    
    return added_rows



############################ sample execution code



# Sample data load (replace this with your actual CSV loading)
# df = pd.read_csv('historic_data/BTCUSDT-1m-2020-01-01.csv')

# Detect missing data
# missing_rows_before = detect_missing_data(df)

# Fill missing data
# df_filled = fill_missing_data(df)

# Find added rows
# added_rows = find_added_rows(df, df_filled)

# if not added_rows.empty:
#     print("The following rows were added:")
#     print(added_rows)
# else:
#     print("No rows were added, meaning no gaps were detected initially or all gaps were present in the original dataset.")

# # Detect missing data again to confirm filling
# missing_rows_after = detect_missing_data(df_filled)

# if missing_rows_after.empty:
#     print("All missing data has been successfully filled.")
# else:
#     print("There are still some missing data issues.")