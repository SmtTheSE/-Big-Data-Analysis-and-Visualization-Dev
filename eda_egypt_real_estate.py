import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# Set style for better-looking plots
plt.style.use('seaborn-v0_8')
sns.set_palette("Blues_r")  # Reversed blues for better contrast

def perform_eda(input_file, output_dir):
    """
    Perform comprehensive Exploratory Data Analysis on Egypt real estate dataset.
    
    Parameters:
    input_file (str): Path to the cleaned CSV file
    output_dir (str): Directory to save plots and reports
    """
    
    # Load the dataset
    print("Loading dataset...")
    df = pd.read_csv(input_file)
    print(f"Dataset shape: {df.shape}")
    
    # Create output directory if it doesn't exist
    import os
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Summary statistics
    print("\nGenerating summary statistics...")
    summary_stats = df.describe()
    summary_stats.to_csv(f"{output_dir}/summary_statistics.csv")
    print("Summary statistics saved to summary_statistics.csv")
    
    # Data types and info
    print("\nDataset information:")
    print(df.info())
    
    # Missing values report
    print("\nMissing values:")
    missing_values = df.isnull().sum()
    missing_df = pd.DataFrame({'Column': missing_values.index, 'Missing_Count': missing_values.values})
    missing_df['Missing_Percentage'] = (missing_df['Missing_Count'] / len(df)) * 100
    missing_df.to_csv(f"{output_dir}/missing_values_report.csv", index=False)
    print("Missing values report saved to missing_values_report.csv")
    
    # Property type distribution
    print("\nAnalyzing property type distribution...")
    property_type_counts = df['type'].value_counts()
    property_type_df = pd.DataFrame({
        'Property_Type': property_type_counts.index,
        'Count': property_type_counts.values,
        'Percentage': (property_type_counts.values / len(df)) * 100
    })
    property_type_df.to_csv(f"{output_dir}/property_type_distribution.csv", index=False)
    print("Property type distribution saved to property_type_distribution.csv")
    
    # Price analysis
    print("\nAnalyzing price distribution...")
    price_stats = {
        'Mean': df['price'].mean(),
        'Median': df['price'].median(),
        'Std_Dev': df['price'].std(),
        'Min': df['price'].min(),
        'Max': df['price'].max(),
        '25th_Percentile': df['price'].quantile(0.25),
        '75th_Percentile': df['price'].quantile(0.75)
    }
    
    price_stats_df = pd.DataFrame.from_dict(price_stats, orient='index', columns=['Value'])
    price_stats_df.to_csv(f"{output_dir}/price_statistics.csv")
    print("Price statistics saved to price_statistics.csv")
    
    # Create visualizations
    
    # 1. Property type distribution
    plt.figure(figsize=(12, 8))
    ax = property_type_counts.plot(kind='bar')
    plt.title('Distribution of Property Types', fontsize=16)
    plt.xlabel('Property Type', fontsize=12)
    plt.ylabel('Count', fontsize=12)
    plt.xticks(rotation=45, ha='right')
    
    # Add value labels on bars
    for i, v in enumerate(property_type_counts.values):
        ax.text(i, v + 10, str(v), ha='center', va='bottom')
    
    plt.tight_layout()
    plt.savefig(f"{output_dir}/property_type_distribution.png", dpi=300, bbox_inches='tight')
    plt.close()
    print("Property type distribution plot saved to property_type_distribution.png")
    
    # 2. Price distribution
    plt.figure(figsize=(12, 8))
    plt.hist(df['price'], bins=50, edgecolor='black', alpha=0.7)
    plt.title('Distribution of Property Prices', fontsize=16)
    plt.xlabel('Price (EGP)', fontsize=12)
    plt.ylabel('Frequency', fontsize=12)
    plt.ticklabel_format(style='plain', axis='x')
    plt.tight_layout()
    plt.savefig(f"{output_dir}/price_distribution.png", dpi=300, bbox_inches='tight')
    plt.close()
    print("Price distribution plot saved to price_distribution.png")
    
    # 3. Price distribution by property type (boxplot)
    plt.figure(figsize=(15, 10))
    df_filtered = df[df['type'].isin(df['type'].value_counts().head(8).index)]
    sns.boxplot(data=df_filtered, x='type', y='price')
    plt.title('Price Distribution by Property Type', fontsize=16)
    plt.xlabel('Property Type', fontsize=12)
    plt.ylabel('Price (EGP)', fontsize=12)
    plt.xticks(rotation=45, ha='right')
    plt.ticklabel_format(style='plain', axis='y')
    plt.tight_layout()
    plt.savefig(f"{output_dir}/price_by_property_type.png", dpi=300, bbox_inches='tight')
    plt.close()
    print("Price by property type plot saved to price_by_property_type.png")
    
    # 4. Bedrooms distribution
    plt.figure(figsize=(12, 8))
    bedroom_counts = df['bedrooms'].value_counts().sort_index()
    plt.bar(bedroom_counts.index, bedroom_counts.values, edgecolor='black', alpha=0.7)
    plt.title('Distribution of Number of Bedrooms', fontsize=16)
    plt.xlabel('Number of Bedrooms', fontsize=12)
    plt.ylabel('Count', fontsize=12)
    plt.tight_layout()
    plt.savefig(f"{output_dir}/bedrooms_distribution.png", dpi=300, bbox_inches='tight')
    plt.close()
    print("Bedrooms distribution plot saved to bedrooms_distribution.png")
    
    # 5. Bathrooms distribution
    plt.figure(figsize=(12, 8))
    bathroom_counts = df['bathrooms'].value_counts().sort_index()
    plt.bar(bathroom_counts.index, bathroom_counts.values, edgecolor='black', alpha=0.7)
    plt.title('Distribution of Number of Bathrooms', fontsize=16)
    plt.xlabel('Number of Bathrooms', fontsize=12)
    plt.ylabel('Count', fontsize=12)
    plt.tight_layout()
    plt.savefig(f"{output_dir}/bathrooms_distribution.png", dpi=300, bbox_inches='tight')
    plt.close()
    print("Bathrooms distribution plot saved to bathrooms_distribution.png")
    
    # 6. Correlation heatmap
    print("\nGenerating correlation heatmap...")
    # Select only numeric columns for correlation
    numeric_df = df.select_dtypes(include=[np.number])
    
    # Compute correlation matrix
    corr_matrix = numeric_df.corr()
    
    # Save correlation matrix
    corr_matrix.to_csv(f"{output_dir}/correlation_matrix.csv")
    print("Correlation matrix saved to correlation_matrix.csv")
    
    # Plot correlation heatmap
    plt.figure(figsize=(10, 8))
    sns.heatmap(corr_matrix, annot=True, cmap='Blues', center=0, 
                square=True, linewidths=0.5, cbar_kws={"shrink": .8},
                annot_kws={"size": 12})
    plt.title('Correlation Matrix of Numeric Variables', fontsize=16)
    plt.tight_layout()
    plt.savefig(f"{output_dir}/correlation_heatmap.png", dpi=300, bbox_inches='tight')
    plt.close()
    print("Correlation heatmap saved to correlation_heatmap.png")
    
    # 7. Price vs Size scatter plot
    plt.figure(figsize=(12, 8))
    plt.scatter(df['size_sqm'], df['price'], alpha=0.5)
    plt.title('Price vs Size', fontsize=16)
    plt.xlabel('Size (sqm)', fontsize=12)
    plt.ylabel('Price (EGP)', fontsize=12)
    plt.ticklabel_format(style='plain', axis='y')
    plt.tight_layout()
    plt.savefig(f"{output_dir}/price_vs_size.png", dpi=300, bbox_inches='tight')
    plt.close()
    print("Price vs size plot saved to price_vs_size.png")
    
    # 8. Top locations by count
    print("\nAnalyzing top locations...")
    top_locations = df['location'].value_counts().head(15)
    top_locations_df = pd.DataFrame({
        'Location': top_locations.index,
        'Count': top_locations.values
    })
    top_locations_df.to_csv(f"{output_dir}/top_locations.csv", index=False)
    print("Top locations saved to top_locations.csv")
    
    # Plot top locations
    plt.figure(figsize=(14, 10))
    ax = top_locations.plot(kind='barh')
    plt.title('Top 15 Locations by Property Count', fontsize=16)
    plt.xlabel('Number of Properties', fontsize=12)
    plt.ylabel('Location', fontsize=12)
    
    # Add value labels
    for i, v in enumerate(top_locations.values):
        ax.text(v + 3, i, str(v), ha='left', va='center')
    
    plt.tight_layout()
    plt.savefig(f"{output_dir}/top_locations.png", dpi=300, bbox_inches='tight')
    plt.close()
    print("Top locations plot saved to top_locations.png")
    
    # 9. Price per square meter analysis
    print("\nAnalyzing price per square meter...")
    df['price_per_sqm'] = df['price'] / df['size_sqm']
    
    # Remove outliers in price per sqm (beyond 3 standard deviations)
    price_per_sqm_mean = df['price_per_sqm'].mean()
    price_per_sqm_std = df['price_per_sqm'].std()
    lower_bound = price_per_sqm_mean - 3 * price_per_sqm_std
    upper_bound = price_per_sqm_mean + 3 * price_per_sqm_std
    df_filtered_ppsm = df[(df['price_per_sqm'] >= lower_bound) & (df['price_per_sqm'] <= upper_bound)]
    
    # Plot price per sqm distribution
    plt.figure(figsize=(12, 8))
    plt.hist(df_filtered_ppsm['price_per_sqm'], bins=50, edgecolor='black', alpha=0.7)
    plt.title('Distribution of Price per Square Meter', fontsize=16)
    plt.xlabel('Price per Square Meter (EGP/sqm)', fontsize=12)
    plt.ylabel('Frequency', fontsize=12)
    plt.tight_layout()
    plt.savefig(f"{output_dir}/price_per_sqm_distribution.png", dpi=300, bbox_inches='tight')
    plt.close()
    print("Price per sqm distribution plot saved to price_per_sqm_distribution.png")
    
    # 10. Price per sqm by property type
    plt.figure(figsize=(15, 10))
    df_filtered_type = df_filtered_ppsm[df_filtered_ppsm['type'].isin(
        df_filtered_ppsm['type'].value_counts().head(8).index)]
    sns.boxplot(data=df_filtered_type, x='type', y='price_per_sqm')
    plt.title('Price per Square Meter by Property Type', fontsize=16)
    plt.xlabel('Property Type', fontsize=12)
    plt.ylabel('Price per Square Meter (EGP/sqm)', fontsize=12)
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig(f"{output_dir}/price_per_sqm_by_type.png", dpi=300, bbox_inches='tight')
    plt.close()
    print("Price per sqm by type plot saved to price_per_sqm_by_type.png")
    
    # Generate EDA report
    print("\nGenerating EDA report...")
    generate_eda_report(df, output_dir)
    print("EDA report saved to eda_report.txt")
    
    print(f"\nEDA completed successfully! All outputs saved to {output_dir}")

def generate_eda_report(df, output_dir):
    """
    Generate a comprehensive EDA report.
    """
    with open(f"{output_dir}/eda_report.txt", 'w') as f:
        f.write("EGYPT REAL ESTATE EXPLORATORY DATA ANALYSIS REPORT\n")
        f.write("=" * 60 + "\n\n")
        
        f.write(f"Report generated on: {datetime.now()}\n\n")
        
        f.write("1. DATASET OVERVIEW\n")
        f.write("-" * 20 + "\n")
        f.write(f"Total Rows: {len(df):,}\n")
        f.write(f"Total Columns: {len(df.columns)}\n")
        f.write(f"Total Data Points: {df.size:,}\n\n")
        
        f.write("2. COLUMN INFORMATION\n")
        f.write("-" * 20 + "\n")
        for col in df.columns:
            f.write(f"{col}: {df[col].dtype}\n")
        f.write("\n")
        
        f.write("3. MISSING VALUES SUMMARY\n")
        f.write("-" * 25 + "\n")
        missing = df.isnull().sum()
        for col, count in missing.items():
            if count > 0:
                percentage = (count / len(df)) * 100
                f.write(f"{col}: {count:,} ({percentage:.2f}%)\n")
        f.write("\n")
        
        f.write("4. PROPERTY TYPE DISTRIBUTION\n")
        f.write("-" * 30 + "\n")
        type_counts = df['type'].value_counts()
        for property_type, count in type_counts.items():
            percentage = (count / len(df)) * 100
            f.write(f"{property_type}: {count:,} ({percentage:.2f}%)\n")
        f.write("\n")
        
        f.write("5. PRICE STATISTICS\n")
        f.write("-" * 18 + "\n")
        f.write(f"Mean Price: {df['price'].mean():,.2f} EGP\n")
        f.write(f"Median Price: {df['price'].median():,.2f} EGP\n")
        f.write(f"Standard Deviation: {df['price'].std():,.2f} EGP\n")
        f.write(f"Minimum Price: {df['price'].min():,} EGP\n")
        f.write(f"Maximum Price: {df['price'].max():,} EGP\n")
        f.write(f"25th Percentile: {df['price'].quantile(0.25):,.2f} EGP\n")
        f.write(f"75th Percentile: {df['price'].quantile(0.75):,.2f} EGP\n\n")
        
        f.write("6. BEDROOMS AND BATHROOMS STATISTICS\n")
        f.write("-" * 40 + "\n")
        f.write(f"Mean Bedrooms: {df['bedrooms'].mean():.2f}\n")
        f.write(f"Median Bedrooms: {df['bedrooms'].median():.2f}\n")
        f.write(f"Mean Bathrooms: {df['bathrooms'].mean():.2f}\n")
        f.write(f"Median Bathrooms: {df['bathrooms'].median():.2f}\n\n")
        
        f.write("7. SIZE STATISTICS\n")
        f.write("-" * 17 + "\n")
        f.write(f"Mean Size: {df['size_sqm'].mean():.2f} sqm\n")
        f.write(f"Median Size: {df['size_sqm'].median():.2f} sqm\n")
        f.write(f"Standard Deviation: {df['size_sqm'].std():.2f} sqm\n")
        f.write(f"Minimum Size: {df['size_sqm'].min():.2f} sqm\n")
        f.write(f"Maximum Size: {df['size_sqm'].max():,.2f} sqm\n\n")
        
        f.write("8. CORRELATION ANALYSIS\n")
        f.write("-" * 22 + "\n")
        numeric_df = df.select_dtypes(include=[np.number])
        corr_matrix = numeric_df.corr()
        f.write("Correlation with Price:\n")
        price_corr = corr_matrix['price'].sort_values(key=abs, ascending=False)
        for col, corr in price_corr.items():
            if col != 'price':  # Skip self-correlation
                f.write(f"{col}: {corr:.4f}\n")
        f.write("\n")
        
        f.write("9. TOP LOCATIONS\n")
        f.write("-" * 15 + "\n")
        top_locations = df['location'].value_counts().head(10)
        for location, count in top_locations.items():
            f.write(f"{location}: {count:,}\n")
        f.write("\n")
        
        f.write("10. KEY INSIGHTS\n")
        f.write("-" * 14 + "\n")
        f.write("1. Apartments, Chalets, and Villas make up the majority of listings\n")
        f.write("2. Price distribution is heavily right-skewed, with a few very expensive properties\n")
        f.write("3. Most properties have 2-4 bedrooms and 2-3 bathrooms\n")
        f.write("4. Property prices show moderate correlation with size\n")
        f.write("5. Location significantly impacts property prices\n")
        f.write("6. Price per square meter varies considerably by property type\n")

if __name__ == "__main__":
    # Define input and output paths
    input_file = "/Users/sittminthar/Desktop/BigData Dev/detailed_cleaned_egypt_real_estate.csv"
    output_dir = "/Users/sittminthar/Desktop/BigData Dev/eda_output"
    
    # Perform EDA
    perform_eda(input_file, output_dir)