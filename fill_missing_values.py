import pandas as pd
import numpy as np

def fill_missing_values(input_file, output_file):
    """
    Fill missing values in the Egypt real estate dataset intelligently.
    
    Parameters:
    input_file (str): Path to the input CSV file
    output_file (str): Path to save the filled CSV file
    
    Returns:
    pd.DataFrame: DataFrame with filled missing values
    """
    
    # Load the dataset
    print("Loading dataset...")
    df = pd.read_csv(input_file)
    print(f"Original dataset shape: {df.shape}")
    
    # Display initial missing values
    print("\nInitial missing values:")
    missing_initial = df.isnull().sum()
    for col, count in missing_initial.items():
        if count > 0:
            percentage = (count / len(df)) * 100
            print(f"  {col}: {count} ({percentage:.2f}%)")
    
    # Fill missing description with "No description provided"
    df['description'] = df['description'].fillna("No description provided")
    
    # Fill missing payment_method with "Not specified"
    df['payment_method'] = df['payment_method'].fillna("Not specified")
    
    # Fill missing bedrooms with median value based on property type
    print("\nFilling missing bedrooms...")
    # Calculate median bedrooms for each property type
    median_bedrooms = df.groupby('type')['bedrooms'].median()
    print("Median bedrooms by property type:")
    for property_type, median in median_bedrooms.items():
        print(f"  {property_type}: {median}")
    
    # Fill missing bedrooms based on property type
    for property_type in df['type'].unique():
        if pd.isna(property_type):
            continue
        mask = (df['type'] == property_type) & (df['bedrooms'].isnull())
        df.loc[mask, 'bedrooms'] = median_bedrooms[property_type]
    
    # Fill remaining missing bedrooms with overall median
    overall_median_bedrooms = df['bedrooms'].median()
    df['bedrooms'] = df['bedrooms'].fillna(overall_median_bedrooms)
    
    # Fill missing bathrooms with median value based on property type
    print("\nFilling missing bathrooms...")
    # Calculate median bathrooms for each property type
    median_bathrooms = df.groupby('type')['bathrooms'].median()
    print("Median bathrooms by property type:")
    for property_type, median in median_bathrooms.items():
        print(f"  {property_type}: {median}")
    
    # Fill missing bathrooms based on property type
    for property_type in df['type'].unique():
        if pd.isna(property_type):
            continue
        mask = (df['type'] == property_type) & (df['bathrooms'].isnull())
        df.loc[mask, 'bathrooms'] = median_bathrooms[property_type]
    
    # Fill remaining missing bathrooms with overall median
    overall_median_bathrooms = df['bathrooms'].median()
    df['bathrooms'] = df['bathrooms'].fillna(overall_median_bathrooms)
    
    # Fill missing available_from with "Available immediately"
    df['available_from'] = df['available_from'].fillna("Available immediately")
    
    # Fill missing down_payment with 0 (assuming no down payment required)
    df['down_payment'] = df['down_payment'].fillna("0")
    
    # Fill missing size_sqm with median value based on property type and bedrooms
    print("\nFilling missing size_sqm...")
    # Calculate median size for each property type and bedroom combination
    median_size = df.groupby(['type', 'bedrooms'])['size_sqm'].median()
    print(f"Unique combinations for size calculation: {len(median_size)}")
    
    # Fill missing size_sqm based on property type and bedrooms
    filled_count = 0
    for (property_type, bedrooms), median in median_size.items():
        if pd.isna(property_type) or pd.isna(bedrooms):
            continue
        mask = (df['type'] == property_type) & (df['bedrooms'] == bedrooms) & (df['size_sqm'].isnull())
        filled = mask.sum()
        if filled > 0:
            df.loc[mask, 'size_sqm'] = median
            filled_count += filled
    
    print(f"Filled {filled_count} size_sqm values based on property type and bedrooms")
    
    # Fill remaining missing size_sqm with median based on property type only
    remaining_missing = df['size_sqm'].isnull().sum()
    if remaining_missing > 0:
        print(f"Filling {remaining_missing} remaining missing size_sqm values based on property type...")
        median_size_by_type = df.groupby('type')['size_sqm'].median()
        for property_type, median in median_size_by_type.items():
            if pd.isna(property_type):
                continue
            mask = (df['type'] == property_type) & (df['size_sqm'].isnull())
            df.loc[mask, 'size_sqm'] = median
    
    # Fill any remaining missing size_sqm with overall median
    overall_median_size = df['size_sqm'].median()
    df['size_sqm'] = df['size_sqm'].fillna(overall_median_size)
    
    # Final check
    print("\nFinal missing values check:")
    missing_final = df.isnull().sum()
    any_missing = False
    for col, count in missing_final.items():
        if count > 0:
            percentage = (count / len(df)) * 100
            print(f"  {col}: {count} ({percentage:.2f}%)")
            any_missing = True
    
    if not any_missing:
        print("  No missing values found!")
    
    # Save the filled dataset
    df.to_csv(output_file, index=False)
    print(f"\nDataset with filled missing values saved to: {output_file}")
    print(f"Final dataset shape: {df.shape}")
    
    return df

if __name__ == "__main__":
    # Define input and output file paths
    input_file = "/Users/sittminthar/Desktop/BigData Dev/detailed_cleaned_egypt_real_estate.csv"
    output_file = "/Users/sittminthar/Desktop/BigData Dev/filled_egypt_real_estate.csv"
    
    # Fill missing values
    filled_df = fill_missing_values(input_file, output_file)
    
    print("\nMissing value filling process completed successfully!")