import os
import pandas as pd
import numpy as np

def clean_and_transform():
    raw_path = os.path.join('data', 'raw', 'sample_-_superstore.xls')
    clean_dir = os.path.join('data', 'clean')
    os.makedirs(clean_dir, exist_ok=True)
    
    print(f"Loading raw data from: {raw_path}")
    df = pd.read_excel(raw_path)
    
    # Ensure proper datetime formats
    df['Order Date'] = pd.to_datetime(df['Order Date'])
    df['Ship Date'] = pd.to_datetime(df['Ship Date'])
    
    # Feature Engineering
    df['Shipping_Days'] = (df['Ship Date'] - df['Order Date']).dt.days
    df['Profit_Margin'] = np.where(df['Sales'] > 0, (df['Profit'] / df['Sales']) * 100, 0)
    df['Is_Loss'] = df['Profit'] < 0
    df['Order_Year'] = df['Order Date'].dt.year
    df['Order_Month'] = df['Order Date'].dt.month
    df['Order_Year_Month'] = df['Order Date'].dt.strftime('%Y-%m')
    df['Order_Quarter'] = df['Order Date'].dt.to_period('Q').astype(str)
    
    # Discount Categories
    bins = [-0.01, 0.001, 0.15, 0.30, 0.50, 1.0]
    labels = ['0% (No Discount)', '1-15% Low', '16-30% Moderate', '31-50% High', '>50% Heavy']
    df['Discount_Category'] = pd.cut(df['Discount'], bins=bins, labels=labels)
    
    # Clean output path
    clean_csv = os.path.join(clean_dir, 'superstore_cleaned.csv')
    df.to_csv(clean_csv, index=False)
    print(f"Successfully processed {len(df)} records and saved to {clean_csv}")
    
    return df

if __name__ == '__main__':
    clean_and_transform()
