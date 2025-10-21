import pandas as pd

def generate_filled_data_quality_report(input_file, report_file):
    """
    Generate a data quality report for the filled dataset.
    
    Parameters:
    input_file (str): Path to the filled CSV file
    report_file (str): Path to save the quality report
    """
    
    # Load the dataset
    df = pd.read_csv(input_file)
    
    with open(report_file, 'w') as f:
        f.write("EGYPT REAL ESTATE DATA QUALITY REPORT (FILLED DATASET)\n")
        f.write("=" * 55 + "\n\n")
        
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
        any_missing = False
        for col, count in missing.items():
            if count > 0:
                percentage = (count / len(df)) * 100
                f.write(f"{col}: {count} ({percentage:.2f}%)\n")
                any_missing = True
        
        if not any_missing:
            f.write("No missing values found in the dataset!\n")
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
    
    print(f"Data quality report for filled dataset saved to: {report_file}")

if __name__ == "__main__":
    # Define input and output file paths
    input_file = "/Users/sittminthar/Desktop/BigData Dev/filled_egypt_real_estate.csv"
    report_file = "/Users/sittminthar/Desktop/BigData Dev/filled_data_quality_report.txt"
    
    # Generate quality report
    generate_filled_data_quality_report(input_file, report_file)
    
    print("\nData quality report generation completed successfully!")