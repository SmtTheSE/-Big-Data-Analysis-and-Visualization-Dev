import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import base64
import os

# Set style for better-looking plots
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")

# Configure the page
st.set_page_config(
    page_title="Egypt Real Estate Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

def load_data():
    """Load the cleaned dataset"""
    try:
        # Try to load data with different possible paths
        possible_paths = [
            "detailed_cleaned_egypt_real_estate.csv",
            "/Users/sittminthar/Desktop/BigData Dev/detailed_cleaned_egypt_real_estate.csv",
            os.path.join(os.path.dirname(__file__), "detailed_cleaned_egypt_real_estate.csv")
        ]
        
        df = None
        for path in possible_paths:
            try:
                if os.path.exists(path):
                    df = pd.read_csv(path)
                    break
            except:
                continue
                
        if df is None:
            st.error("Dataset file not found. Please make sure the file exists.")
            return None
        return df
    except Exception as e:
        st.error(f"Error loading dataset: {str(e)}")
        return None

def load_eda_data():
    """Load EDA data"""
    eda_dir = "eda_output"
    possible_paths = [
        eda_dir,
        "/Users/sittminthar/Desktop/BigData Dev/eda_output",
        os.path.join(os.path.dirname(__file__), "eda_output")
    ]
    
    # Find the correct EDA directory
    correct_eda_dir = None
    for path in possible_paths:
        if os.path.exists(path):
            correct_eda_dir = path
            break
    
    if correct_eda_dir is None:
        st.warning("EDA files not found. Some visualizations may not be available.")
        return None, None, None, None, None, None
    
    try:
        summary_stats = pd.read_csv(f"{correct_eda_dir}/summary_statistics.csv")
        correlation_matrix = pd.read_csv(f"{correct_eda_dir}/correlation_matrix.csv")
        missing_values = pd.read_csv(f"{correct_eda_dir}/missing_values_report.csv")
        property_type_dist = pd.read_csv(f"{correct_eda_dir}/property_type_distribution.csv")
        price_stats = pd.read_csv(f"{correct_eda_dir}/price_statistics.csv")
        top_locations = pd.read_csv(f"{correct_eda_dir}/top_locations.csv")
        return summary_stats, correlation_matrix, missing_values, property_type_dist, price_stats, top_locations
    except FileNotFoundError:
        st.warning("Some EDA files are missing. Some visualizations may not be available.")
        return None, None, None, None, None, None

def main():
    # Title and description
    st.title("Egypt Real Estate Dashboard")
    st.markdown("""
    This dashboard presents a comprehensive analysis of the Egypt real estate market.
    Navigate through the tabs to explore different aspects of the data.
    """)
    
    # Load data
    df = load_data()
    if df is None:
        st.stop()
    
    # Load EDA data
    summary_stats, correlation_matrix, missing_values, property_type_dist, price_stats, top_locations = load_eda_data()
    
    # Create tabs
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "Overview", 
        "PropertyParams", 
        "Price Analysis", 
        "Size Analysis", 
        "Location Analysis", 
        "Correlations"
    ])
    
    # Tab 1: Overview
    with tab1:
        st.header("Dataset Overview")
        
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Total Properties", f"{len(df):,}")
        col2.metric("Attributes", len(df.columns))
        col3.metric("Data Points", f"{df.size:,}")
        col4.metric("Data Completeness", f"{((df.size - df.isnull().sum().sum()) / df.size) * 100:.1f}%")
        
        st.subheader("Property Types Distribution")
        if property_type_dist is not None:
            st.dataframe(property_type_dist)
        else:
            st.write("Property type distribution data not available.")
        
        # Create a bar chart of property types
        fig, ax = plt.subplots(figsize=(10, 6))
        property_counts = df['type'].value_counts().head(10)
        ax.bar(property_counts.index, property_counts.values)
        ax.set_title("Top 10 Property Types")
        ax.set_xlabel("Property Type")
        ax.set_ylabel("Count")
        plt.xticks(rotation=45, ha='right')
        st.pyplot(fig)
        
        st.subheader("Missing Values Report")
        if missing_values is not None:
            st.dataframe(missing_values)
        else:
            st.write("Missing values data not available.")
    
    # Tab 2: Property Attributes
    with tab2:
        st.header("PropertyParams Analysis")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Bedrooms Distribution")
            fig, ax = plt.subplots(figsize=(8, 6))
            bedroom_counts = df['bedrooms'].value_counts().sort_index()
            ax.bar(bedroom_counts.index, bedroom_counts.values)
            ax.set_xlabel("Number of Bedrooms")
            ax.set_ylabel("Count")
            st.pyplot(fig)
            
            st.metric("Average Bedrooms", f"{df['bedrooms'].mean():.2f}")
            st.metric("Median Bedrooms", f"{df['bedrooms'].median():.0f}")
        
        with col2:
            st.subheader("Bathrooms Distribution")
            fig, ax = plt.subplots(figsize=(8, 6))
            bathroom_counts = df['bathrooms'].value_counts().sort_index()
            ax.bar(bathroom_counts.index, bathroom_counts.values)
            ax.set_xlabel("Number of Bathrooms")
            ax.set_ylabel("Count")
            st.pyplot(fig)
            
            st.metric("Average Bathrooms", f"{df['bathrooms'].mean():.2f}")
            st.metric("Median Bathrooms", f"{df['bathrooms'].median():.0f}")
    
    # Tab 3: Price Analysis
    with tab3:
        st.header("Price Analysis")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Price Statistics")
            if price_stats is not None:
                st.dataframe(price_stats)
            else:
                # Calculate basic stats if file not available
                price_stats_data = {
                    'Statistic': ['Mean', 'Median', 'Min', 'Max'],
                    'Value': [f"{df['price'].mean():,.2f}", f"{df['price'].median():,.2f}", 
                             f"{df['price'].min():,}", f"{df['price'].max():,}"]
                }
                st.dataframe(pd.DataFrame(price_stats_data))
            
        with col2:
            st.subheader("Price Distribution")
            fig, ax = plt.subplots(figsize=(10, 6))
            ax.hist(df['price'], bins=50, edgecolor='black', alpha=0.7)
            ax.set_xlabel("Price (EGP)")
            ax.set_ylabel("Frequency")
            ax.set_title("Distribution of Property Prices")
            st.pyplot(fig)
        
        st.subheader("Price by Property Type")
        fig, ax = plt.subplots(figsize=(12, 8))
        df_filtered = df[df['type'].isin(df['type'].value_counts().head(8).index)]
        df_grouped = df_filtered.groupby('type')['price'].agg(['mean', 'median']).sort_values('mean', ascending=False)
        ax.bar(df_grouped.index, df_grouped['mean'], label='Mean', alpha=0.7)
        ax.bar(df_grouped.index, df_grouped['median'], label='Median', alpha=0.7)
        ax.set_xlabel("Property Type")
        ax.set_ylabel("Price (EGP)")
        ax.set_title("Average and Median Price by Property Type")
        ax.legend()
        plt.xticks(rotation=45, ha='right')
        st.pyplot(fig)
    
    # Tab 4: Size Analysis
    with tab4:
        st.header("PropertyParams Size Analysis")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric("Average Size", f"{df['size_sqm'].mean():,.2f} sqm")
            st.metric("Median Size", f"{df['size_sqm'].median():,.0f} sqm")
            st.metric("Min Size", f"{df['size_sqm'].min():,.0f} sqm")
            st.metric("Max Size", f"{df['size_sqm'].max():,.0f} sqm")
        
        with col2:
            st.subheader("Size Distribution")
            fig, ax = plt.subplots(figsize=(10, 6))
            ax.hist(df['size_sqm'], bins=50, edgecolor='black', alpha=0.7)
            ax.set_xlabel("Size (sqm)")
            ax.set_ylabel("Frequency")
            ax.set_title("Distribution of Property Sizes")
            st.pyplot(fig)
        
        st.subheader("Price per Square Meter")
        df['price_per_sqm'] = df['price'] / df['size_sqm']
        fig, ax = plt.subplots(figsize=(12, 8))
        ax.hist(df['price_per_sqm'], bins=50, edgecolor='black', alpha=0.7)
        ax.set_xlabel("Price per Square Meter (EGP/sqm)")
        ax.set_ylabel("Frequency")
        ax.set_title("Distribution of Price per Square Meter")
        st.pyplot(fig)
    
    # Tab 5: Location Analysis
    with tab5:
        st.header("PropertyParams Location Analysis")
        
        st.subheader("Top Locations")
        if top_locations is not None:
            st.dataframe(top_locations)
        else:
            st.write("Top locations data not available.")
        
        st.subheader("Properties by Location")
        fig, ax = plt.subplots(figsize=(12, 8))
        top_locations_plot = df['location'].value_counts().head(15)
        ax.barh(top_locations_plot.index, top_locations_plot.values)
        ax.set_xlabel("Number of Properties")
        ax.set_ylabel("Location")
        ax.set_title("Top 15 Locations by Property Count")
        st.pyplot(fig)
    
    # Tab 6: Correlations
    with tab6:
        st.header("PropertyParams Correlations")
        
        if correlation_matrix is not None:
            st.subheader("Correlation Matrix")
            st.dataframe(correlation_matrix)
            
            st.subheader("Correlation Heatmap")
            fig, ax = plt.subplots(figsize=(10, 8))
            # Create a heatmap using seaborn
            corr_data = correlation_matrix.set_index(correlation_matrix.columns[0])
            sns.heatmap(corr_data, annot=True, cmap='coolwarm', center=0, square=True, linewidths=0.5)
            ax.set_title('Correlation Matrix of Numeric Variables')
            st.pyplot(fig)
        else:
            st.warning("Correlation data not available.")
    
    # Footer
    st.markdown("---")
    st.markdown(f"**Dashboard generated on:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == "__main__":
    main()