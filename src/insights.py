import pandas as pd
import numpy as np

def generate_bi_insights(df):
    if df.empty:
        return {
            'total_sales': 0, 'total_profit': 0, 'profit_margin': 0,
            'total_orders': 0, 'avg_order_val': 0, 'loss_percentage': 0,
            'insights_list': ["No data available for the selected filters."]
        }
        
    total_sales = df['Sales'].sum()
    total_profit = df['Profit'].sum()
    profit_margin = (total_profit / total_sales * 100) if total_sales > 0 else 0
    total_orders = df['Order ID'].nunique()
    avg_order_val = total_sales / total_orders if total_orders > 0 else 0
    
    loss_df = df[df['Is_Loss']]
    total_rows = len(df)
    loss_rows = len(loss_df)
    loss_percentage = (loss_rows / total_rows * 100) if total_rows > 0 else 0
    total_loss_amount = abs(loss_df['Profit'].sum())
    
    # Best & Worst Category
    cat_summary = df.groupby('Category')['Profit'].sum().sort_values(ascending=False)
    best_cat = cat_summary.index[0] if not cat_summary.empty else 'N/A'
    best_cat_profit = cat_summary.iloc[0] if not cat_summary.empty else 0
    
    # Subcategory breakdown
    subcat_summary = df.groupby('Sub-Category')['Profit'].sum().sort_values(ascending=False)
    best_subcat = subcat_summary.index[0] if not subcat_summary.empty else 'N/A'
    worst_subcat = subcat_summary.index[-1] if not subcat_summary.empty else 'N/A'
    worst_subcat_profit = subcat_summary.iloc[-1] if not subcat_summary.empty else 0
    
    # High discount impact
    high_disc_df = df[df['Discount'] >= 0.30]
    high_disc_loss = abs(high_disc_df[high_disc_df['Profit'] < 0]['Profit'].sum())
    
    # Regional top
    region_summary = df.groupby('Region')['Sales'].sum().sort_values(ascending=False)
    top_region = region_summary.index[0] if not region_summary.empty else 'N/A'
    
    insights = []
    
    # Insight 1: Profit Margin & Health
    if profit_margin > 12:
        insights.append({
            'type': 'success',
            'title': 'Strong Overall Profitability',
            'text': f"Overall Profit Margin is healthy at **{profit_margin:.2f}%** generating **${total_profit:,.2f}** total profit across {total_orders:,} orders."
        })
    elif profit_margin > 5:
        insights.append({
            'type': 'warning',
            'title': 'Moderate Profit Margin',
            'text': f"Overall Profit Margin stands at **{profit_margin:.2f}%**. Consider optimizing high-discount sub-categories."
        })
    else:
        insights.append({
            'type': 'danger',
            'title': 'Critical Margin Alert',
            'text': f"Profit Margin is low at **{profit_margin:.2f}%**. Heavy discounting is eroding net profits."
        })
        
    # Insight 2: Loss Leakage & Discount Warning
    if loss_percentage > 0:
        insights.append({
            'type': 'danger',
            'title': 'Profit Leakage & Discount Impact',
            'text': f"**{loss_percentage:.1f}%** of transactions ({loss_rows:,} orders) are operating at a net loss, totaling **${total_loss_amount:,.2f}** in lost profits. Discounts >= 30% account for **${high_disc_loss:,.2f}** of these losses."
        })
        
    # Insight 3: Category Highlights
    insights.append({
        'type': 'info',
        'title': 'Category & Sub-Category Champions',
        'text': f"**{best_cat}** is the top-performing Category delivering **${best_cat_profit:,.2f}** in profit. **{best_subcat}** is the most profitable sub-category, while **{worst_subcat}** generated the highest loss (**${worst_subcat_profit:,.2f}**)."
    })
    
    # Insight 4: Regional Contribution
    insights.append({
        'type': 'info',
        'title': 'Regional Revenue Leadership',
        'text': f"The **{top_region} Region** leads total revenue with **${region_summary.iloc[0]:,.2f}** in sales."
    })
    
    # Strategic Recommendations
    recommendations = [
        f"**Cap Maximum Discounts on {worst_subcat}**: Restrict discounts over 20% on items in the '{worst_subcat}' sub-category to prevent immediate margin loss.",
        f"**Promote Top Margin Category**: Double down on marketing and inventory allocation for **{best_cat}**.",
        "**Tiered Shipping Controls**: Review standard vs express shipping costs for low-value orders to increase average basket margin."
    ]
    
    return {
        'total_sales': total_sales,
        'total_profit': total_profit,
        'profit_margin': profit_margin,
        'total_orders': total_orders,
        'avg_order_val': avg_order_val,
        'loss_percentage': loss_percentage,
        'total_loss_amount': total_loss_amount,
        'insights': insights,
        'recommendations': recommendations
    }
