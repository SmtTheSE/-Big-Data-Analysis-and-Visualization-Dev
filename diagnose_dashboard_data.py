import pandas as pd
import os

def load_data():
    """Replicate the exact loading function from the dashboard"""
    # Try to load data with different possible paths
    possible_paths = [
        "latest_cleaned_egypt_real_estate.csv",
        "/Users/sittminthar/Desktop/BigData Dev/latest_cleaned_egypt_real_estate.csv",
        "filled_egypt_real_estate.csv",
        "/Users/sittminthar/Desktop/BigData Dev/filled_egypt_real_estate.csv",
        "detailed_cleaned_egypt_real_estate.csv",
        "/Users/sittminthar/Desktop/BigData Dev/detailed_cleaned_egypt_real_estate.csv",
        "cleaned_egypt_real_estate.csv",
        "/Users/sittminthar/Desktop/BigData Dev/cleaned_egypt_real_estate.csv"
    ]
    
    df = None
    loaded_file = None
    for path in possible_paths:
        try:
            if os.path.exists(path):
                df = pd.read_csv(path)
                loaded_file = path
                print(f"Successfully loaded: {path}")
                print(f"Dataset shape: {df.shape}")
                print(f"Missing values: {df.isnull().sum().sum()}")
                
                # Show specific column missing values
                print("\nMissing values by column:")
                for col in df.columns:
                    missing_count = df[col].isnull().sum()
                    if missing_count > 0:
                        print(f"  {col}: {missing_count}")
                break
            else:
                print(f"File not found: {path}")
        except Exception as e:
            print(f"Error loading {path}: {e}")
            continue
            
    if df is None:
        print("No dataset file found!")
        return None
    return df

# Run the function
df = load_data()