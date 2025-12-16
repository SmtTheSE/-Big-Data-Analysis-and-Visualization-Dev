#!/usr/bin/env python3
"""
Medical Insurance Cost Prediction Analysis Script

This script performs exploratory data analysis, visualization, and predictive modeling
on a medical insurance dataset containing records for 100,000 individuals.
The approach uses demographic-based train/test splits and modern ML techniques
to simulate real-world application scenarios.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error
from sklearn.utils import resample
import xgboost as xgb
import warnings
warnings.filterwarnings('ignore')

# Set plotting style
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")

def load_and_explore_data():
    """
    Load the medical insurance dataset and perform initial exploration
    """
    # Load the dataset
    df = pd.read_csv('[Final Project]medical_insurance.csv')
    
    # Display basic information
    print("Dataset Shape:", df.shape)
    print("\nColumn Names:")
    print(df.columns.tolist())
    
    # Display first few rows
    print("\nFirst 5 Rows:")
    print(df.head())
    
    # Basic statistics
    print("\nBasic Statistics:")
    print(df.describe())
    
    # Check for missing values
    print("\nMissing Values:")
    print(df.isnull().sum())
    
    return df

def visualize_data_distribution(df):
    """
    Create visualizations to understand data distribution
    """
    # Set up the plotting area
    fig, axes = plt.subplots(2, 2, figsize=(15, 12))
    fig.suptitle('Medical Insurance Data Distribution', fontsize=16)
    
    # Age distribution
    axes[0, 0].hist(df['age'], bins=50, color='skyblue', edgecolor='black')
    axes[0, 0].set_title('Age Distribution')
    axes[0, 0].set_xlabel('Age')
    axes[0, 0].set_ylabel('Frequency')
    
    # BMI distribution
    axes[0, 1].hist(df['bmi'], bins=50, color='lightgreen', edgecolor='black')
    axes[0, 1].set_title('BMI Distribution')
    axes[0, 1].set_xlabel('BMI')
    axes[0, 1].set_ylabel('Frequency')
    
    # Annual medical cost distribution
    axes[1, 0].hist(df['annual_medical_cost'], bins=50, color='salmon', edgecolor='black')
    axes[1, 0].set_title('Annual Medical Cost Distribution')
    axes[1, 0].set_xlabel('Annual Medical Cost ($)')
    axes[1, 0].set_ylabel('Frequency')
    
    # Smoking status distribution
    smoking_counts = df['smoker'].value_counts()
    axes[1, 1].bar(smoking_counts.index, smoking_counts.values, color=['coral', 'gold', 'lightseagreen'])
    axes[1, 1].set_title('Smoking Status Distribution')
    axes[1, 1].set_xlabel('Smoking Status')
    axes[1, 1].set_ylabel('Count')
    
    plt.tight_layout()
    plt.savefig('data_distribution.png', dpi=300, bbox_inches='tight')
    plt.show()

def analyze_cost_relationships(df):
    """
    Analyze relationships between key variables and medical costs
    """
    # Set up the plotting area
    fig, axes = plt.subplots(2, 2, figsize=(15, 12))
    fig.suptitle('Relationships Between Variables and Medical Costs', fontsize=16)
    
    # Age vs Medical Cost
    axes[0, 0].scatter(df['age'], df['annual_medical_cost'], alpha=0.5, color='purple')
    axes[0, 0].set_title('Age vs Annual Medical Cost')
    axes[0, 0].set_xlabel('Age')
    axes[0, 0].set_ylabel('Annual Medical Cost ($)')
    
    # BMI vs Medical Cost
    axes[0, 1].scatter(df['bmi'], df['annual_medical_cost'], alpha=0.5, color='orange')
    axes[0, 1].set_title('BMI vs Annual Medical Cost')
    axes[0, 1].set_xlabel('BMI')
    axes[0, 1].set_ylabel('Annual Medical Cost ($)')
    
    # Box plot of costs by smoking status
    df.boxplot(column='annual_medical_cost', by='smoker', ax=axes[1, 0])
    axes[1, 0].set_title('Medical Costs by Smoking Status')
    axes[1, 0].set_xlabel('Smoking Status')
    axes[1, 0].set_ylabel('Annual Medical Cost ($)')
    
    # Average cost by number of chronic conditions
    chronic_costs = df.groupby('chronic_count')['annual_medical_cost'].mean()
    axes[1, 1].bar(chronic_costs.index, chronic_costs.values, color='teal')
    axes[1, 1].set_title('Average Medical Cost by Number of Chronic Conditions')
    axes[1, 1].set_xlabel('Number of Chronic Conditions')
    axes[1, 1].set_ylabel('Average Annual Medical Cost ($)')
    
    plt.tight_layout()
    plt.savefig('cost_relationships.png', dpi=300, bbox_inches='tight')
    plt.show()

def prepare_features(df):
    """
    Prepare features for machine learning models
    """
    # Select relevant features
    feature_columns = [
        'age', 'sex', 'bmi', 'smoker', 'chronic_count', 
        'hypertension', 'diabetes', 'region', 'income',
        'education', 'marital_status', 'employment_status'
    ]
    
    # Create feature dataframe
    X = df[feature_columns].copy()
    
    # Target variable
    y = df['annual_medical_cost']
    
    # Handle categorical variables
    categorical_columns = ['sex', 'smoker', 'region', 'education', 'marital_status', 'employment_status']
    
    # Encode categorical variables
    le_dict = {}
    for col in categorical_columns:
        le = LabelEncoder()
        X[col] = le.fit_transform(X[col].astype(str))
        le_dict[col] = le
    
    return X, y, le_dict

def demographic_split_train_test(X, y, df, split_criteria='sex'):
    """
    Split data based on demographic criteria for more realistic evaluation
    """
    if split_criteria == 'sex':
        # Train on male, test on female (or vice versa)
        train_indices = df[df['sex'] == 'Male'].index
        test_indices = df[df['sex'] == 'Female'].index
    elif split_criteria == 'region':
        # Train on North region, test on others
        train_indices = df[df['region'] == 'North'].index
        test_indices = df[df['region'] != 'North'].index
    elif split_criteria == 'age':
        # Train on younger population (< 50), test on older (>= 50)
        train_indices = df[df['age'] < 50].index
        test_indices = df[df['age'] >= 50].index
    else:
        # Default random split if criteria not recognized
        train_indices = df.sample(frac=0.8, random_state=42).index
        test_indices = df.drop(train_indices).index
    
    X_train, X_test = X.loc[train_indices], X.loc[test_indices]
    y_train, y_test = y.loc[train_indices], y.loc[test_indices]
    
    print(f"Training set size: {len(X_train)}")
    print(f"Test set size: {len(X_test)}")
    
    return X_train, X_test, y_train, y_test

def apply_smote(X_train, y_train):
    """
    Apply SMOTE to handle any imbalanced aspects of the training data
    Note: SMOTE is typically used for classification, but we can adapt the concept
    by oversampling high-cost cases which are underrepresented
    """
    # For regression, we'll create a synthetic oversampling approach
    # Identify high-cost cases (top 10% of costs)
    threshold = np.percentile(y_train, 90)
    high_cost_indices = y_train[y_train >= threshold].index
    normal_cost_indices = y_train[y_train < threshold].index
    
    # Oversample high-cost cases to balance the dataset
    if len(high_cost_indices) > 0:
        # Calculate oversampling ratio
        oversample_ratio = min(int(len(normal_cost_indices) / len(high_cost_indices)), 3)
        
        # Create oversampled data
        high_cost_X = X_train.loc[high_cost_indices]
        high_cost_y = y_train.loc[high_cost_indices]
        
        # Combine original with oversampled data
        X_train_balanced = pd.concat([X_train] + [high_cost_X] * oversample_ratio, axis=0)
        y_train_balanced = pd.concat([y_train] + [high_cost_y] * oversample_ratio, axis=0)
        
        print(f"Balanced training set size: {len(X_train_balanced)}")
        return X_train_balanced, y_train_balanced
    
    return X_train, y_train

def build_predictive_models(X_train, y_train, X_test, y_test):
    """
    Build and evaluate predictive models using modern ML techniques
    """
    # Scale features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # Convert to DataFrame to preserve index/columns
    X_train_scaled = pd.DataFrame(X_train_scaled, columns=X_train.columns, index=X_train.index)
    X_test_scaled = pd.DataFrame(X_test_scaled, columns=X_test.columns, index=X_test.index)
    
    # Initialize models
    models = {
        'Linear Regression': LinearRegression(),
        'Gradient Boosting': GradientBoostingRegressor(n_estimators=100, random_state=42),
        'XGBoost': xgb.XGBRegressor(n_estimators=100, random_state=42)
    }
    
    results = {}
    
    # Train and evaluate each model
    for name, model in models.items():
        print(f"\nTraining {name}...")
        model.fit(X_train_scaled, y_train)
        y_pred = model.predict(X_test_scaled)
        
        # Calculate metrics
        r2 = r2_score(y_test, y_pred)
        rmse = np.sqrt(mean_squared_error(y_test, y_pred))
        mae = mean_absolute_error(y_test, y_pred)
        
        results[name] = {
            'model': model,
            'r2': r2,
            'rmse': rmse,
            'mae': mae,
            'predictions': y_pred
        }
        
        print(f"{name} - R²: {r2:.4f}, RMSE: ${rmse:,.2f}, MAE: ${mae:,.2f}")
    
    # Compare models
    print("\nModel Comparison:")
    comparison_df = pd.DataFrame({
        'Model': list(results.keys()),
        'R²': [results[model]['r2'] for model in results.keys()],
        'RMSE': [results[model]['rmse'] for model in results.keys()],
        'MAE': [results[model]['mae'] for model in results.keys()]
    })
    
    print(comparison_df.sort_values('R²', ascending=False))
    
    # Select best model based on R²
    best_model_name = comparison_df.loc[comparison_df['R²'].idxmax(), 'Model']
    print(f"\nBest performing model: {best_model_name}")
    
    # Feature importance for the best model (if applicable)
    best_model = results[best_model_name]['model']
    if hasattr(best_model, 'feature_importances_'):
        feature_importance = pd.DataFrame({
            'feature': X_train.columns,
            'importance': best_model.feature_importances_
        }).sort_values('importance', ascending=False)
        
        print(f"\nFeature Importance ({best_model_name}):")
        print(feature_importance)
        
        # Visualize feature importance
        plt.figure(figsize=(10, 6))
        sns.barplot(data=feature_importance.head(10), x='importance', y='feature', palette='viridis')
        plt.title(f'Top 10 Feature Importance - {best_model_name}')
        plt.xlabel('Importance Score')
        plt.ylabel('Features')
        plt.tight_layout()
        plt.savefig('feature_importance.png', dpi=300, bbox_inches='tight')
        plt.show()
    
    return results, best_model_name

def real_world_evaluation(df, results, best_model_name, X_test, y_test):
    """
    Perform real-world evaluation of models
    """
    print("\nReal-World Evaluation:")
    
    # Get predictions from best model
    best_predictions = results[best_model_name]['predictions']
    
    # Calculate prediction accuracy by demographic groups
    test_indices = X_test.index
    test_df = df.loc[test_indices].copy()
    test_df['predicted_cost'] = best_predictions
    test_df['actual_cost'] = y_test
    
    # Evaluate by sex
    sex_performance = test_df.groupby('sex').apply(
        lambda x: pd.Series({
            'R²': r2_score(x['actual_cost'], x['predicted_cost']),
            'MAE': mean_absolute_error(x['actual_cost'], x['predicted_cost']),
            'RMSE': np.sqrt(mean_squared_error(x['actual_cost'], x['predicted_cost']))
        })
    )
    
    print("Performance by Sex:")
    print(sex_performance)
    
    # Evaluate by age groups
    test_df['age_group'] = pd.cut(test_df['age'], bins=[0, 30, 50, 70, 100], labels=['Young', 'Middle', 'Senior', 'Elderly'])
    age_performance = test_df.groupby('age_group').apply(
        lambda x: pd.Series({
            'R²': r2_score(x['actual_cost'], x['predicted_cost']),
            'MAE': mean_absolute_error(x['actual_cost'], x['predicted_cost']),
            'RMSE': np.sqrt(mean_squared_error(x['actual_cost'], x['predicted_cost']))
        })
    )
    
    print("\nPerformance by Age Group:")
    print(age_performance)
    
    # Evaluate by cost quartiles
    test_df['cost_quartile'] = pd.qcut(test_df['actual_cost'], q=4, labels=['Q1', 'Q2', 'Q3', 'Q4'])
    cost_performance = test_df.groupby('cost_quartile').apply(
        lambda x: pd.Series({
            'R²': r2_score(x['actual_cost'], x['predicted_cost']),
            'MAE': mean_absolute_error(x['actual_cost'], x['predicted_cost']),
            'RMSE': np.sqrt(mean_squared_error(x['actual_cost'], x['predicted_cost']))
        })
    )
    
    print("\nPerformance by Cost Quartile:")
    print(cost_performance)

def main():
    """
    Main function to run the complete analysis
    """
    print("Loading and exploring data...")
    df = load_and_explore_data()
    
    print("\nCreating visualizations...")
    visualize_data_distribution(df)
    analyze_cost_relationships(df)
    
    print("\nPreparing features...")
    X, y, le_dict = prepare_features(df)
    
    print("\nSplitting data by demographic criteria...")
    X_train, X_test, y_train, y_test = demographic_split_train_test(X, y, df, split_criteria='sex')
    
    print("\nApplying SMOTE-like balancing technique...")
    X_train_balanced, y_train_balanced = apply_smote(X_train, y_train)
    
    print("\nBuilding predictive models...")
    results, best_model_name = build_predictive_models(X_train_balanced, y_train_balanced, X_test, y_test)
    
    print("\nPerforming real-world evaluation...")
    real_world_evaluation(df, results, best_model_name, X_test, y_test)
    
    print("\nAnalysis complete! Check the generated plots for visual insights.")

if __name__ == "__main__":
    main()