import pandas as pd
import os

# Check all possible CSV files in the directory
print("Checking all CSV files in the directory:")
for file in os.listdir("/Users/sittminthar/Desktop/BigData Dev"):
    if file.endswith(".csv"):
        try:
            filepath = os.path.join("/Users/sittminthar/Desktop/BigData Dev", file)
            df = pd.read_csv(filepath)
            missing_bedrooms = df['bedrooms'].isnull().sum() if 'bedrooms' in df.columns else 'N/A'
            print(f"  {file}: {df.shape} - Missing bedrooms: {missing_bedrooms}")
        except Exception as e:
            print(f"  {file}: Error reading file - {e}")

print("\nChecking specifically for the missing values pattern you mentioned:")
target_missing = {
    'description': 1,
    'bedrooms': 432,
    'bathrooms': 150,
    'available_from': 533,
    'payment_method': 1,
    'down_payment': 13733
}

for file in os.listdir("/Users/sittminthar/Desktop/BigData Dev"):
    if file.endswith(".csv"):
        try:
            filepath = os.path.join("/Users/sittminthar/Desktop/BigData Dev", file)
            df = pd.read_csv(filepath)
            if all(col in df.columns for col in target_missing.keys()):
                matches = True
                for col, expected_missing in target_missing.items():
                    actual_missing = df[col].isnull().sum()
                    if actual_missing != expected_missing:
                        matches = False
                        break
                
                if matches:
                    print(f"  FOUND MATCH: {file}")
                    print(f"    Shape: {df.shape}")
                    total_missing = df.isnull().sum().sum()
                    print(f"    Total missing values: {total_missing}")
                    break
        except Exception as e:
            continue
else:
    print("  No file found matching the missing values pattern.")