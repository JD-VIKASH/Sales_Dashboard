import os
import pandas as pd

def load_data(filepath=None):
    if filepath is None:
        filepath = os.path.join('data', 'clean', 'superstore_cleaned.csv')
        if not os.path.exists(filepath):
            # Fallback if cleaning hasn't run
            from scripts.clean_data import clean_and_transform
            return clean_and_transform()
            
    df = pd.read_csv(filepath)
    df['Order Date'] = pd.to_datetime(df['Order Date'])
    df['Ship Date'] = pd.to_datetime(df['Ship Date'])
    return df

def filter_dataframe(df, date_range=None, regions=None, categories=None, subcategories=None, segments=None, discount_ranges=None):
    filtered_df = df.copy()
    
    if date_range and len(date_range) == 2:
        start_date, end_date = date_range
        filtered_df = filtered_df[
            (filtered_df['Order Date'].dt.date >= start_date) & 
            (filtered_df['Order Date'].dt.date <= end_date)
        ]
        
    if regions:
        filtered_df = filtered_df[filtered_df['Region'].isin(regions)]
        
    if categories:
        filtered_df = filtered_df[filtered_df['Category'].isin(categories)]
        
    if subcategories:
        filtered_df = filtered_df[filtered_df['Sub-Category'].isin(subcategories)]
        
    if segments:
        filtered_df = filtered_df[filtered_df['Segment'].isin(segments)]
        
    if discount_ranges:
        filtered_df = filtered_df[filtered_df['Discount_Category'].isin(discount_ranges)]
        
    return filtered_df
