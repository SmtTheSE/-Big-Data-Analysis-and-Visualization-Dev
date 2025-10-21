import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# Set style for better-looking plots
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")

def create_dashboard(cleaned_data_file, eda_output_dir, dashboard_output_dir):
    """
    Create a comprehensive dashboard summarizing data cleaning and EDA results.
    
    Parameters:
    cleaned_data_file (str): Path to the cleaned CSV file
    eda_output_dir (str): Directory containing EDA outputs
    dashboard_output_dir (str): Directory to save dashboard outputs
    """
    
    # Create output directory if it doesn't exist
    import os
    if not os.path.exists(dashboard_output_dir):
        os.makedirs(dashboard_output_dir)
    
    # Load the cleaned dataset
    print("Loading cleaned dataset...")
    df = pd.read_csv(cleaned_data_file)
    print(f"Dataset shape: {df.shape}")
    
    # Create dashboard figures
    
    # 1. Data Overview Dashboard
    fig1 = plt.figure(figsize=(16, 12))
    fig1.suptitle('Egypt Real Estate Data Analysis Dashboard', fontsize=20, fontweight='bold')
    
    # Dataset Overview
    ax1 = plt.subplot2grid((4, 4), (0, 0), colspan=2)
    ax1.text(0.1, 0.9, f"Total Properties: {len(df):,}", fontsize=14, fontweight='bold')
    ax1.text(0.1, 0.7, f"Total Columns: {len(df.columns)}", fontsize=14, fontweight='bold')
    ax1.text(0.1, 0.5, f"Total Data Points: {df.size:,}", fontsize=14, fontweight='bold')
    ax1.text(0.1, 0.3, f"Missing Data: {df.isnull().sum().sum():,}", fontsize=14, fontweight='bold')
    ax1.set_title('Dataset Overview', fontsize=16, fontweight='bold')
    ax1.axis('off')
    
    # Property Type Distribution (Text)
    ax2 = plt.subplot2grid((4, 4), (0, 2), colspan=2)
    type_counts = df['type'].value_counts()
    top_types = type_counts.head(5)
    ax2.text(0.1, 0.9, "Top Property Types:", fontsize=14, fontweight='bold')
    for i, (ptype, count) in enumerate(top_types.items()):
        pct = (count / len(df)) * 100
        ax2.text(0.1, 0.7 - i*0.15, f"{ptype}: {count:,} ({pct:.1f}%)", fontsize=12)
    ax2.set_title('Property Type Distribution', fontsize=16, fontweight='bold')
    ax2.axis('off')
    
    # Price Statistics
    ax3 = plt.subplot2grid((4, 4), (1, 0), colspan=2)
    ax3.text(0.1, 0.9, f"Mean Price: {df['price'].mean():,.0f} EGP", fontsize=12)
    ax3.text(0.1, 0.7, f"Median Price: {df['price'].median():,.0f} EGP", fontsize=12)
    ax3.text(0.1, 0.5, f"Min Price: {df['price'].min():,} EGP", fontsize=12)
    ax3.text(0.1, 0.3, f"Max Price: {df['price'].max():,} EGP", fontsize=12)
    ax3.set_title('Price Statistics', fontsize=16, fontweight='bold')
    ax3.axis('off')
    
    # Bedrooms and Bathrooms Statistics
    ax4 = plt.subplot2grid((4, 4), (1, 2), colspan=2)
    ax4.text(0.1, 0.9, f"Mean Bedrooms: {df['bedrooms'].mean():.2f}", fontsize=12)
    ax4.text(0.1, 0.7, f"Median Bedrooms: {df['bedrooms'].median():.0f}", fontsize=12)
    ax4.text(0.1, 0.5, f"Mean Bathrooms: {df['bathrooms'].mean():.2f}", fontsize=12)
    ax4.text(0.1, 0.3, f"Median Bathrooms: {df['bathrooms'].median():.0f}", fontsize=12)
    ax4.set_title('Bedrooms & Bathrooms', fontsize=16, fontweight='bold')
    ax4.axis('off')
    
    # Load and display property type distribution chart
    try:
        img1 = plt.imread(f"{eda_output_dir}/property_type_distribution.png")
        ax5 = plt.subplot2grid((4, 4), (2, 0), colspan=2)
        ax5.imshow(img1)
        ax5.set_title('Property Types Distribution', fontsize=14, fontweight='bold')
        ax5.axis('off')
    except:
        ax5 = plt.subplot2grid((4, 4), (2, 0), colspan=2)
        ax5.text(0.5, 0.5, 'Property Type Distribution Chart\n(Not Available)', 
                ha='center', va='center', fontsize=12)
        ax5.set_title('Property Types Distribution', fontsize=14, fontweight='bold')
        ax5.axis('off')
    
    # Load and display price distribution chart
    try:
        img2 = plt.imread(f"{eda_output_dir}/price_distribution.png")
        ax6 = plt.subplot2grid((4, 4), (2, 2), colspan=2)
        ax6.imshow(img2)
        ax6.set_title('Price Distribution', fontsize=14, fontweight='bold')
        ax6.axis('off')
    except:
        ax6 = plt.subplot2grid((4, 4), (2, 2), colspan=2)
        ax6.text(0.5, 0.5, 'Price Distribution Chart\n(Not Available)', 
                ha='center', va='center', fontsize=12)
        ax6.set_title('Price Distribution', fontsize=14, fontweight='bold')
        ax6.axis('off')
    
    # Load and display top locations chart
    try:
        img3 = plt.imread(f"{eda_output_dir}/top_locations.png")
        ax7 = plt.subplot2grid((4, 4), (3, 0), colspan=2)
        ax7.imshow(img3)
        ax7.set_title('Top Locations', fontsize=14, fontweight='bold')
        ax7.axis('off')
    except:
        ax7 = plt.subplot2grid((4, 4), (3, 0), colspan=2)
        ax7.text(0.5, 0.5, 'Top Locations Chart\n(Not Available)', 
                ha='center', va='center', fontsize=12)
        ax7.set_title('Top Locations', fontsize=14, fontweight='bold')
        ax7.axis('off')
    
    # Load and display correlation heatmap
    try:
        img4 = plt.imread(f"{eda_output_dir}/correlation_heatmap.png")
        ax8 = plt.subplot2grid((4, 4), (3, 2), colspan=2)
        ax8.imshow(img4)
        ax8.set_title('Correlation Heatmap', fontsize=14, fontweight='bold')
        ax8.axis('off')
    except:
        ax8 = plt.subplot2grid((4, 4), (3, 2), colspan=2)
        ax8.text(0.5, 0.5, 'Correlation Heatmap\n(Not Available)', 
                ha='center', va='center', fontsize=12)
        ax8.set_title('Correlation Heatmap', fontsize=14, fontweight='bold')
        ax8.axis('off')
    
    plt.tight_layout()
    plt.savefig(f"{dashboard_output_dir}/dashboard_overview.png", dpi=300, bbox_inches='tight')
    plt.close()
    print("Dashboard overview saved to dashboard_overview.png")
    
    # 2. Detailed Analysis Dashboard
    fig2 = plt.figure(figsize=(16, 12))
    fig2.suptitle('Detailed Analysis Dashboard', fontsize=20, fontweight='bold')
    
    # Price by Property Type
    try:
        img5 = plt.imread(f"{eda_output_dir}/price_by_property_type.png")
        ax9 = plt.subplot2grid((3, 3), (0, 0), colspan=2)
        ax9.imshow(img5)
        ax9.set_title('Price Distribution by Property Type', fontsize=14, fontweight='bold')
        ax9.axis('off')
    except:
        ax9 = plt.subplot2grid((3, 3), (0, 0), colspan=2)
        ax9.text(0.5, 0.5, 'Price by Property Type Chart\n(Not Available)', 
                ha='center', va='center', fontsize=12)
        ax9.set_title('Price Distribution by Property Type', fontsize=14, fontweight='bold')
        ax9.axis('off')
    
    # Bedrooms Distribution
    try:
        img6 = plt.imread(f"{eda_output_dir}/bedrooms_distribution.png")
        ax10 = plt.subplot2grid((3, 3), (0, 2))
        ax10.imshow(img6)
        ax10.set_title('Bedrooms Distribution', fontsize=14, fontweight='bold')
        ax10.axis('off')
    except:
        ax10 = plt.subplot2grid((3, 3), (0, 2))
        ax10.text(0.5, 0.5, 'Bedrooms Distribution Chart\n(Not Available)', 
                ha='center', va='center', fontsize=12)
        ax10.set_title('Bedrooms Distribution', fontsize=14, fontweight='bold')
        ax10.axis('off')
    
    # Bathrooms Distribution
    try:
        img7 = plt.imread(f"{eda_output_dir}/bathrooms_distribution.png")
        ax11 = plt.subplot2grid((3, 3), (1, 0))
        ax11.imshow(img7)
        ax11.set_title('Bathrooms Distribution', fontsize=14, fontweight='bold')
        ax11.axis('off')
    except:
        ax11 = plt.subplot2grid((3, 3), (1, 0))
        ax11.text(0.5, 0.5, 'Bathrooms Distribution Chart\n(Not Available)', 
                ha='center', va='center', fontsize=12)
        ax11.set_title('Bathrooms Distribution', fontsize=14, fontweight='bold')
        ax11.axis('off')
    
    # Price vs Size
    try:
        img8 = plt.imread(f"{eda_output_dir}/price_vs_size.png")
        ax12 = plt.subplot2grid((3, 3), (1, 1))
        ax12.imshow(img8)
        ax12.set_title('Price vs Size', fontsize=14, fontweight='bold')
        ax12.axis('off')
    except:
        ax12 = plt.subplot2grid((3, 3), (1, 1))
        ax12.text(0.5, 0.5, 'Price vs Size Chart\n(Not Available)', 
                ha='center', va='center', fontsize=12)
        ax12.set_title('Price vs Size', fontsize=14, fontweight='bold')
        ax12.axis('off')
    
    # Price per Square Meter Distribution
    try:
        img9 = plt.imread(f"{eda_output_dir}/price_per_sqm_distribution.png")
        ax13 = plt.subplot2grid((3, 3), (1, 2))
        ax13.imshow(img9)
        ax13.set_title('Price per Square Meter', fontsize=14, fontweight='bold')
        ax13.axis('off')
    except:
        ax13 = plt.subplot2grid((3, 3), (1, 2))
        ax13.text(0.5, 0.5, 'Price per Square Meter Chart\n(Not Available)', 
                ha='center', va='center', fontsize=12)
        ax13.set_title('Price per Square Meter', fontsize=14, fontweight='bold')
        ax13.axis('off')
    
    # Price per Square Meter by Type
    try:
        img10 = plt.imread(f"{eda_output_dir}/price_per_sqm_by_type.png")
        ax14 = plt.subplot2grid((3, 3), (2, 0), colspan=3)
        ax14.imshow(img10)
        ax14.set_title('Price per Square Meter by Property Type', fontsize=14, fontweight='bold')
        ax14.axis('off')
    except:
        ax14 = plt.subplot2grid((3, 3), (2, 0), colspan=3)
        ax14.text(0.5, 0.5, 'Price per Square Meter by Type Chart\n(Not Available)', 
                ha='center', va='center', fontsize=12)
        ax14.set_title('Price per Square Meter by Property Type', fontsize=14, fontweight='bold')
        ax14.axis('off')
    
    plt.tight_layout()
    plt.savefig(f"{dashboard_output_dir}/dashboard_detailed.png", dpi=300, bbox_inches='tight')
    plt.close()
    print("Detailed dashboard saved to dashboard_detailed.png")
    
    # 3. Summary Report
    create_summary_report(df, eda_output_dir, dashboard_output_dir)
    print("Summary report saved to dashboard_summary.txt")
    
    print(f"\nDashboard creation completed! All outputs saved to {dashboard_output_dir}")

def create_summary_report(df, eda_output_dir, dashboard_output_dir):
    """
    Create a text summary report of the dashboard findings.
    """
    with open(f"{dashboard_output_dir}/dashboard_summary.txt", 'w') as f:
        f.write("EGYPT REAL ESTATE ANALYSIS DASHBOARD SUMMARY\n")
        f.write("=" * 50 + "\n\n")
        
        f.write(f"Report generated on: {datetime.now()}\n\n")
        
        f.write("1. DATASET OVERVIEW\n")
        f.write("-" * 18 + "\n")
        f.write(f"Total Properties Analyzed: {len(df):,}\n")
        f.write(f"Total Attributes: {len(df.columns)}\n")
        f.write(f"Total Data Points: {df.size:,}\n")
        f.write(f"Missing Data Points: {df.isnull().sum().sum():,}\n\n")
        
        f.write("2. PROPERTY TYPES\n")
        f.write("-" * 15 + "\n")
        type_counts = df['type'].value_counts()
        for i, (ptype, count) in enumerate(type_counts.head(5).items()):
            pct = (count / len(df)) * 100
            f.write(f"{i+1}. {ptype}: {count:,} ({pct:.1f}%)\n")
        f.write("\n")
        
        f.write("3. PRICE ANALYSIS\n")
        f.write("-" * 15 + "\n")
        f.write(f"Average Price: {df['price'].mean():,.0f} EGP\n")
        f.write(f"Median Price: {df['price'].median():,.0f} EGP\n")
        f.write(f"Price Range: {df['price'].min():,} - {df['price'].max():,} EGP\n")
        f.write(f"Standard Deviation: {df['price'].std():,.0f} EGP\n\n")
        
        f.write("4. PROPERTY CHARACTERISTICS\n")
        f.write("-" * 25 + "\n")
        f.write(f"Average Bedrooms: {df['bedrooms'].mean():.2f}\n")
        f.write(f"Median Bedrooms: {df['bedrooms'].median():.0f}\n")
        f.write(f"Average Bathrooms: {df['bathrooms'].mean():.2f}\n")
        f.write(f"Median Bathrooms: {df['bathrooms'].median():.0f}\n")
        f.write(f"Average Size: {df['size_sqm'].mean():.2f} sqm\n")
        f.write(f"Median Size: {df['size_sqm'].median():.0f} sqm\n\n")
        
        f.write("5. KEY INSIGHTS\n")
        f.write("-" * 12 + "\n")
        f.write("1. Apartments, Chalets, and Villas represent the majority of listings\n")
        f.write("2. Price distribution is heavily right-skewed with a few very expensive properties\n")
        f.write("3. Most properties have 2-4 bedrooms and 2-3 bathrooms\n")
        f.write("4. There's a strong correlation between price and number of bedrooms/bathrooms\n")
        f.write("5. Location significantly impacts property prices\n")
        f.write("6. Price per square meter varies considerably by property type\n\n")
        
        f.write("6. TOP LOCATIONS\n")
        f.write("-" * 14 + "\n")
        top_locations = df['location'].value_counts().head(5)
        for i, (location, count) in enumerate(top_locations.items()):
            f.write(f"{i+1}. {location}: {count:,} properties\n")
        f.write("\n")
        
        f.write("7. DATA QUALITY\n")
        f.write("-" * 13 + "\n")
        missing_data = df.isnull().sum()
        total_missing = missing_data.sum()
        f.write(f"Overall Data Completeness: {((df.size - total_missing) / df.size) * 100:.1f}%\n")
        f.write("Columns with Missing Data:\n")
        for col, missing_count in missing_data.items():
            if missing_count > 0:
                pct = (missing_count / len(df)) * 100
                f.write(f"  - {col}: {missing_count:,} ({pct:.1f}%)\n")
        if total_missing == 0:
            f.write("  No missing data found!\n")

if __name__ == "__main__":
    # Define paths
    cleaned_data_file = "/Users/sittminthar/Desktop/BigData Dev/latest_cleaned_egypt_real_estate.csv"
    eda_output_dir = "/Users/sittminthar/Desktop/BigData Dev/eda_output"
    dashboard_output_dir = "/Users/sittminthar/Desktop/BigData Dev/dashboard_output"
    
    # Create dashboard
    create_dashboard(cleaned_data_file, eda_output_dir, dashboard_output_dir)