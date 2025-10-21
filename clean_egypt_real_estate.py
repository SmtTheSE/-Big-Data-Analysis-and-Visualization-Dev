import pandas as pd
import numpy as np
import re

def clean_egypt_real_estate_data(input_file, output_file):
    """
    Smart data cleaning function for Egypt real estate dataset.
    
    Parameters:
    input_file (str): Path to the input CSV file
    output_file (str): Path to save the cleaned CSV file
    
    Returns:
    pd.DataFrame: Cleaned dataframe
    """
    
    # Load the dataset
    print("Loading dataset...")
    df = pd.read_csv(input_file)
    print(f"Original dataset shape: {df.shape}")
    
    # Display initial information
    print("\nDataset Info:")
    print(f"Total rows: {len(df)}")
    print(f"Total columns: {len(df.columns)}")
    print(f"Missing values:\n{df.isnull().sum()}")
    
    # Remove exact duplicate rows
    print("\nRemoving duplicate rows...")
    df_clean = df.drop_duplicates()
    print(f"Shape after removing duplicates: {df_clean.shape}")
    
    # Handle missing values in key columns
    print("\nHandling missing values in key columns...")
    # Remove rows where essential columns are missing
    df_clean = df_clean[df_clean['price'].notnull() & 
                       df_clean['type'].notnull() & 
                       df_clean['location'].notnull()]
    print(f"Shape after removing rows with missing key data: {df_clean.shape}")
    
    # Clean and convert price column
    print("\nCleaning price column...")
    # Remove commas and convert to numeric
    df_clean['price'] = df_clean['price'].astype(str).str.replace(',', '')
    df_clean['price'] = pd.to_numeric(df_clean['price'], errors='coerce')
    
    # Remove rows with invalid prices
    df_clean = df_clean[df_clean['price'].notnull()]
    df_clean['price'] = df_clean['price'].astype('int64')
    print(f"Shape after cleaning price column: {df_clean.shape}")
    
    # Clean bedrooms and bathrooms columns
    print("\nCleaning bedrooms and bathrooms columns...")
    df_clean['bedrooms'] = df_clean['bedrooms'].astype(str).str.replace('+ Maid', '').str.replace(' Maid', '')
    df_clean['bathrooms'] = df_clean['bathrooms'].astype(str).str.replace('+ Maid', '').str.replace(' Maid', '')
    
    # Convert to numeric where possible
    df_clean['bedrooms'] = pd.to_numeric(df_clean['bedrooms'], errors='coerce')
    df_clean['bathrooms'] = pd.to_numeric(df_clean['bathrooms'], errors='coerce')
    
    # Standardize property types
    print("\nStandardizing property types...")
    type_mapping = {
        'Appartment': 'Apartment',
        'appartement': 'Apartment',
        'Appartement': 'Apartment',
        'Chalet ': 'Chalet',
        'Villa ': 'Villa',
        'Duplex ': 'Duplex'
    }
    
    df_clean['type'] = df_clean['type'].replace(type_mapping)
    
    # Clean size column and extract numeric values
    print("\nCleaning size column...")
    # Extract numeric values from size column (e.g., "1,787 sqft / 166 sqm")
    df_clean['size_sqm'] = df_clean['size'].str.extract(r'(\d+(?:,\d+)*)\s*sqm')
    df_clean['size_sqm'] = df_clean['size_sqm'].str.replace(',', '').astype(float)
    
    # Remove outliers in price (values beyond 3 standard deviations)
    print("\nRemoving price outliers...")
    price_mean = df_clean['price'].mean()
    price_std = df_clean['price'].std()
    lower_bound = price_mean - 3 * price_std
    upper_bound = price_mean + 3 * price_std
    
    df_clean = df_clean[(df_clean['price'] >= lower_bound) & 
                       (df_clean['price'] <= upper_bound)]
    print(f"Shape after removing outliers: {df_clean.shape}")
    
    # Final dataset info
    print("\nCleaned Dataset Info:")
    print(f"Final shape: {df_clean.shape}")
    print(f"Missing values in key columns:")
    print(f"- Price: {df_clean['price'].isnull().sum()}")
    print(f"- Type: {df_clean['type'].isnull().sum()}")
    print(f"- Location: {df_clean['location'].isnull().sum()}")
    print(f"- Bedrooms: {df_clean['bedrooms'].isnull().sum()}")
    print(f"- Bathrooms: {df_clean['bathrooms'].isnull().sum()}")
    
    print("\nProperty type distribution:")
    print(df_clean['type'].value_counts())
    
    print("\nPrice statistics:")
    print(f"Min price: {df_clean['price'].min():,}")
    print(f"Max price: {df_clean['price'].max():,}")
    print(f"Mean price: {df_clean['price'].mean():,.2f}")
    print(f"Median price: {df_clean['price'].median():,.2f}")
    
    # Save cleaned dataset
    df_clean.to_csv(output_file, index=False)
    print(f"\nCleaned dataset saved to: {output_file}")
    
    return df_clean

def generate_data_quality_report(df, report_file):
    """
    Generate a data quality report for the cleaned dataset.
    
    Parameters:
    df (pd.DataFrame): Cleaned dataframe
    report_file (str): Path to save the quality report
    """
    
    with open(report_file, 'w') as f:
        f.write("EGYPT REAL ESTATE DATA QUALITY REPORT\n")
        f.write("=" * 50 + "\n\n")
        
        f.write("1. DATASET OVERVIEW\n")
        f.write("-" * 20 + "\n")
        f.write(f"Total Rows: {len(df)}\n")
        f.write(f"Total Columns: {len(df.columns)}\n")
        f.write(f"Total Cells: {df.size}\n\n")
        
        f.write("2. COLUMN INFORMATION\n")
        f.write("-" * 20 + "\n")
        for col in df.columns:
            f.write(f"{col}: {df[col].dtype}\n")
        f.write("\n")
        
        f.write("3. MISSING VALUES\n")
        f.write("-" * 15 + "\n")
        missing = df.isnull().sum()
        for col, count in missing.items():
            if count > 0:
                percentage = (count / len(df)) * 100
                f.write(f"{col}: {count} ({percentage:.2f}%)\n")
        f.write("\n")
        
        f.write("4. DUPLICATE ROWS\n")
        f.write("-" * 15 + "\n")
        duplicates = df.duplicated().sum()
        f.write(f"Duplicate Rows: {duplicates}\n\n")
        
        f.write("5. STATISTICAL SUMMARY\n")
        f.write("-" * 20 + "\n")
        f.write(df.describe().to_string())
        f.write("\n\n")
        
        f.write("6. PROPERTY TYPE DISTRIBUTION\n")
        f.write("-" * 30 + "\n")
        type_counts = df['type'].value_counts()
        for property_type, count in type_counts.items():
            f.write(f"{property_type}: {count}\n")
        f.write("\n")
        
        f.write("7. TOP 10 LOCATIONS\n")
        f.write("-" * 18 + "\n")
        location_counts = df['location'].value_counts().head(10)
        for location, count in location_counts.items():
            f.write(f"{location}: {count}\n")
    
    print(f"Data quality report saved to: {report_file}")

if __name__ == "__main__":
    # Define input and output file paths
    input_file = "/Users/sittminthar/Desktop/BigData Dev/egypt_real_estate_listings.csv"
    output_file = "/Users/sittminthar/Desktop/BigData Dev/cleaned_egypt_real_estate.csv"
    report_file = "/Users/sittminthar/Desktop/BigData Dev/data_quality_report.txt"
    
    # Clean the data
    cleaned_df = clean_egypt_real_estate_data(input_file, output_file)
    
    # Generate quality report
    generate_data_quality_report(cleaned_df, report_file)
    
    print("\nData cleaning process completed successfully!")