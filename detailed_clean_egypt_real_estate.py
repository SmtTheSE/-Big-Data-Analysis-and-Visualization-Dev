import pandas as pd
import numpy as np
import re
from datetime import datetime

def detailed_clean_egypt_real_estate_data(input_file, output_file, log_file):
    """
    Detailed data cleaning function for Egypt real estate dataset with comprehensive logging.
    
    Parameters:
    input_file (str): Path to the input CSV file
    output_file (str): Path to save the cleaned CSV file
    log_file (str): Path to save the detailed log file
    
    Returns:
    pd.DataFrame: Cleaned dataframe
    """
    
    # Initialize log file
    with open(log_file, 'w') as f:
        f.write(f"EGYPT REAL ESTATE DATA CLEANING LOG\n")
        f.write(f"===================================\n")
        f.write(f"Start time: {datetime.now()}\n")
        f.write(f"Input file: {input_file}\n")
        f.write(f"Output file: {output_file}\n\n")
    
    # Load the dataset
    log_message("Loading dataset...", log_file)
    df = pd.read_csv(input_file)
    log_message(f"Original dataset shape: {df.shape}", log_file)
    
    # Display initial information
    log_message("\nDataset Info:", log_file)
    log_message(f"Total rows: {len(df)}", log_file)
    log_message(f"Total columns: {len(df.columns)}", log_file)
    log_message("Missing values:", log_file)
    missing_values = df.isnull().sum()
    for col, count in missing_values.items():
        log_message(f"  {col}: {count}", log_file)
    
    # Check for exact duplicates
    log_message("\nChecking for exact duplicates...", log_file)
    duplicates = df[df.duplicated(keep=False)]
    log_message(f"Number of duplicate rows found: {len(duplicates)}", log_file)
    
    if len(duplicates) > 0:
        # Save duplicates to log file
        duplicates_log_file = output_file.replace('.csv', '_duplicates.csv')
        duplicates.to_csv(duplicates_log_file, index=False)
        log_message(f"Duplicate rows saved to: {duplicates_log_file}", log_file)
        
        # Show sample duplicates in log
        log_message("Sample duplicate rows:", log_file)
        log_message(duplicates.head().to_string(), log_file)
    
    # Remove exact duplicate rows
    log_message("\nRemoving duplicate rows...", log_file)
    df_clean = df.drop_duplicates()
    log_message(f"Shape after removing duplicates: {df_clean.shape}", log_file)
    log_message(f"Removed {len(df) - len(df_clean)} duplicate rows", log_file)
    
    # Handle missing values in key columns
    log_message("\nHandling missing values in key columns...", log_file)
    # Identify rows with missing key data
    missing_key_data = df_clean[df_clean['price'].isnull() | 
                               df_clean['type'].isnull() | 
                               df_clean['location'].isnull()]
    
    log_message(f"Rows with missing key data (price/type/location): {len(missing_key_data)}", log_file)
    
    if len(missing_key_data) > 0:
        # Save rows with missing key data
        missing_key_log_file = output_file.replace('.csv', '_missing_key_data.csv')
        missing_key_data.to_csv(missing_key_log_file, index=False)
        log_message(f"Rows with missing key data saved to: {missing_key_log_file}", log_file)
        
        # Show sample rows with missing key data
        log_message("Sample rows with missing key data:", log_file)
        log_message(missing_key_data.head().to_string(), log_file)
    
    # Remove rows where essential columns are missing
    df_clean = df_clean[df_clean['price'].notnull() & 
                       df_clean['type'].notnull() & 
                       df_clean['location'].notnull()]
    log_message(f"Shape after removing rows with missing key data: {df_clean.shape}", log_file)
    
    # Clean and convert price column
    log_message("\nCleaning price column...", log_file)
    # Check for non-standard price formats
    original_price = df_clean['price'].copy()
    df_clean['price'] = df_clean['price'].astype(str).str.replace(',', '')
    
    # Identify rows with invalid price formats
    invalid_prices = pd.to_numeric(df_clean['price'], errors='coerce').isnull() & (df_clean['price'] != 'nan')
    invalid_price_rows = df_clean[invalid_prices]
    log_message(f"Rows with invalid price formats: {len(invalid_price_rows)}", log_file)
    
    if len(invalid_price_rows) > 0:
        # Save rows with invalid price formats
        invalid_price_log_file = output_file.replace('.csv', '_invalid_prices.csv')
        invalid_price_rows.to_csv(invalid_price_log_file, index=False)
        log_message(f"Rows with invalid price formats saved to: {invalid_price_log_file}", log_file)
        
        # Show sample rows with invalid prices
        log_message("Sample rows with invalid price formats:", log_file)
        log_message(invalid_price_rows.head().to_string(), log_file)
    
    # Convert to numeric
    df_clean['price'] = pd.to_numeric(df_clean['price'], errors='coerce')
    
    # Remove rows with invalid prices
    valid_price_rows = df_clean[df_clean['price'].notnull()]
    log_message(f"Rows with valid prices: {len(valid_price_rows)}", log_file)
    invalid_price_count = len(df_clean) - len(valid_price_rows)
    log_message(f"Rows with invalid prices to be removed: {invalid_price_count}", log_file)
    
    df_clean = valid_price_rows
    df_clean['price'] = df_clean['price'].astype('int64')
    log_message(f"Shape after cleaning price column: {df_clean.shape}", log_file)
    
    # Clean bedrooms and bathrooms columns
    log_message("\nCleaning bedrooms and bathrooms columns...", log_file)
    original_bedrooms = df_clean['bedrooms'].copy()
    original_bathrooms = df_clean['bathrooms'].copy()
    
    df_clean['bedrooms'] = df_clean['bedrooms'].astype(str).str.replace('+ Maid', '').str.replace(' Maid', '').str.strip()
    df_clean['bathrooms'] = df_clean['bathrooms'].astype(str).str.replace('+ Maid', '').str.replace(' Maid', '').str.strip()
    
    # Identify rows with non-numeric values after cleaning
    df_clean['bedrooms'] = pd.to_numeric(df_clean['bedrooms'], errors='coerce')
    df_clean['bathrooms'] = pd.to_numeric(df_clean['bathrooms'], errors='coerce')
    
    # Convert to numeric where possible
    non_numeric_bedrooms = df_clean['bedrooms'].isnull() & (original_bedrooms != 'nan')
    non_numeric_bathrooms = df_clean['bathrooms'].isnull() & (original_bathrooms != 'nan')
    
    log_message(f"Rows with non-numeric bedrooms: {non_numeric_bedrooms.sum()}", log_file)
    log_message(f"Rows with non-numeric bathrooms: {non_numeric_bathrooms.sum()}", log_file)
    
    # Standardize property types
    log_message("\nStandardizing property types...", log_file)
    original_types = df_clean['type'].copy()
    type_mapping = {
        'Appartment': 'Apartment',
        'appartement': 'Apartment',
        'Appartement': 'Apartment',
        'Chalet ': 'Chalet',
        'Villa ': 'Villa',
        'Duplex ': 'Duplex'
    }
    
    df_clean['type'] = df_clean['type'].replace(type_mapping)
    
    # Count changes
    type_changes = (original_types != df_clean['type']).sum()
    log_message(f"Property type standardizations made: {type_changes}", log_file)
    
    # Clean size column and extract numeric values
    log_message("\nCleaning size column...", log_file)
    # Extract numeric values from size column (e.g., "1,787 sqft / 166 sqm")
    df_clean['size_sqm'] = df_clean['size'].str.extract(r'(\d+(?:,\d+)*)\s*sqm')
    df_clean['size_sqm'] = df_clean['size_sqm'].str.replace(',', '').astype(float)
    
    # Remove outliers in price (values beyond 3 standard deviations)
    log_message("\nRemoving price outliers...", log_file)
    price_mean = df_clean['price'].mean()
    price_std = df_clean['price'].std()
    lower_bound = price_mean - 3 * price_std
    upper_bound = price_mean + 3 * price_std
    
    outliers = df_clean[(df_clean['price'] < lower_bound) | 
                       (df_clean['price'] > upper_bound)]
    
    log_message(f"Price outliers found: {len(outliers)}", log_file)
    log_message(f"Price range: {price_mean - 3 * price_std:,.2f} to {price_mean + 3 * price_std:,.2f}", log_file)
    
    if len(outliers) > 0:
        # Save outliers
        outliers_log_file = output_file.replace('.csv', '_price_outliers.csv')
        outliers.to_csv(outliers_log_file, index=False)
        log_message(f"Price outliers saved to: {outliers_log_file}", log_file)
        
        # Show sample outliers
        log_message("Sample price outliers:", log_file)
        log_message(outliers.head().to_string(), log_file)
    
    df_clean = df_clean[(df_clean['price'] >= lower_bound) & 
                       (df_clean['price'] <= upper_bound)]
    log_message(f"Shape after removing outliers: {df_clean.shape}", log_file)
    
    # Final dataset info
    log_message("\nCleaned Dataset Info:", log_file)
    log_message(f"Final shape: {df_clean.shape}", log_file)
    log_message("Missing values in key columns:", log_file)
    log_message(f"- Price: {df_clean['price'].isnull().sum()}", log_file)
    log_message(f"- Type: {df_clean['type'].isnull().sum()}", log_file)
    log_message(f"- Location: {df_clean['location'].isnull().sum()}", log_file)
    log_message(f"- Bedrooms: {df_clean['bedrooms'].isnull().sum()}", log_file)
    log_message(f"- Bathrooms: {df_clean['bathrooms'].isnull().sum()}", log_file)
    
    log_message("\nProperty type distribution:", log_file)
    type_counts = df_clean['type'].value_counts()
    for property_type, count in type_counts.items():
        log_message(f"  {property_type}: {count}", log_file)
    
    log_message("\nPrice statistics:", log_file)
    log_message(f"  Min price: {df_clean['price'].min():,}", log_file)
    log_message(f"  Max price: {df_clean['price'].max():,}", log_file)
    log_message(f"  Mean price: {df_clean['price'].mean():,.2f}", log_file)
    log_message(f"  Median price: {df_clean['price'].median():,.2f}", log_file)
    
    # Save cleaned dataset
    df_clean.to_csv(output_file, index=False)
    log_message(f"\nCleaned dataset saved to: {output_file}", log_file)
    
    # Log completion time
    log_message(f"\nData cleaning process completed at: {datetime.now()}", log_file)
    
    return df_clean

def log_message(message, log_file):
    """
    Write message to both console and log file.
    
    Parameters:
    message (str): Message to log
    log_file (str): Path to log file
    """
    print(message)
    with open(log_file, 'a') as f:
        f.write(message + '\n')

if __name__ == "__main__":
    # Define input and output file paths
    input_file = "/Users/sittminthar/Desktop/BigData Dev/egypt_real_estate_listings.csv"
    output_file = "/Users/sittminthar/Desktop/BigData Dev/detailed_cleaned_egypt_real_estate.csv"
    log_file = "/Users/sittminthar/Desktop/BigData Dev/detailed_cleaning_log.txt"
    
    # Clean the data
    cleaned_df = detailed_clean_egypt_real_estate_data(input_file, output_file, log_file)
    
    print(f"\nDetailed data cleaning process completed successfully!")
    print(f"Cleaned dataset saved to: {output_file}")
    print(f"Detailed log saved to: {log_file}")