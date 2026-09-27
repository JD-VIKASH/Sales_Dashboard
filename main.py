import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

from src.data_loader import load_data, filter_dataframe
from src.insights import generate_bi_insights

# 1. Page Configuration
st.set_page_config(
    page_title="Data Analyst BI Dashboard | Superstore Insights",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Modern BI Aesthetics
st.markdown("""
<style>
    /* Dark Glassmorphism Styling */
    .stApp {
        background-color: #0e1117;
        color: #e0e6ed;
    }
    .metric-card {
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.05), rgba(255, 255, 255, 0.02));
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        padding: 18px 22px;
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.2);
        transition: transform 0.2s ease;
    }
    .metric-card:hover {
        transform: translateY(-3px);
        border-color: #00d2ff;
    }
    .metric-title {
        font-size: 0.88rem;
        color: #94a3b8;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    .metric-value {
        font-size: 1.8rem;
        font-weight: 700;
        color: #ffffff;
        margin-top: 4px;
    }
    .metric-sub {
        font-size: 0.82rem;
        margin-top: 4px;
        font-weight: 500;
    }
    .text-green { color: #10b981; }
    .text-red { color: #ef4444; }
    .text-blue { color: #3b82f6; }
    .text-amber { color: #f59e0b; }
    
    .insight-card {
        padding: 16px 20px;
        border-radius: 10px;
        margin-bottom: 12px;
        border-left: 5px solid;
        background-color: rgba(30, 41, 59, 0.7);
    }
    .insight-card.success { border-left-color: #10b981; }
    .insight-card.info { border-left-color: #3b82f6; }
    .insight-card.warning { border-left-color: #f59e0b; }
    .insight-card.danger { border-left-color: #ef4444; }
    
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px 8px 0 0;
        padding: 10px 20px;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

# 2. Data Loading & Caching
@st.cache_data
def get_cached_data():
    return load_data()

df_raw = get_cached_data()

# 3. Sidebar Filters
st.sidebar.image("https://img.icons8.com/isometric/100/combo-chart.png", width=70)
st.sidebar.title("📊 BI Filters & Controls")
st.sidebar.markdown("---")

# Date Filter
min_date = df_raw['Order Date'].min().date()
max_date = df_raw['Order Date'].max().date()

date_range = st.sidebar.date_input(
    "Select Date Range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)

# Region Filter
all_regions = sorted(df_raw['Region'].unique().tolist())
selected_regions = st.sidebar.multiselect("Regions", options=all_regions, default=all_regions)

# Category & Sub-Category Filter
all_categories = sorted(df_raw['Category'].unique().tolist())
selected_categories = st.sidebar.multiselect("Categories", options=all_categories, default=all_categories)

subcat_options = sorted(df_raw[df_raw['Category'].isin(selected_categories)]['Sub-Category'].unique().tolist())
selected_subcategories = st.sidebar.multiselect("Sub-Categories", options=subcat_options, default=subcat_options)

# Segment Filter
all_segments = sorted(df_raw['Segment'].unique().tolist())
selected_segments = st.sidebar.multiselect("Customer Segments", options=all_segments, default=all_segments)

# Discount Category Filter
all_disc_cats = df_raw['Discount_Category'].cat.categories.tolist() if hasattr(df_raw['Discount_Category'], 'cat') else sorted(df_raw['Discount_Category'].unique().tolist())
selected_disc_cats = st.sidebar.multiselect("Discount Levels", options=all_disc_cats, default=all_disc_cats)

# Filter Dataset
df_filtered = filter_dataframe(
    df_raw,
    date_range=date_range,
    regions=selected_regions,
    categories=selected_categories,
    subcategories=selected_subcategories,
    segments=selected_segments,
    discount_ranges=selected_disc_cats
)

# Generate BI Insights
bi_metrics = generate_bi_insights(df_filtered)

# 4. Header Section
st.title("📈 Business Intelligence & Analytics Dashboard")
st.markdown("### Strategic Performance & Insights for Data Analysts")

st.markdown("---")

# 5. Top KPI Metrics Row
col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">💰 Total Revenue</div>
        <div class="metric-value">${bi_metrics['total_sales']:,.0f}</div>
        <div class="metric-sub text-blue">Filtered Sales</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    profit_color = "text-green" if bi_metrics['total_profit'] >= 0 else "text-red"
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">📈 Net Profit</div>
        <div class="metric-value ${profit_color}">${bi_metrics['total_profit']:,.0f}</div>
        <div class="metric-sub ${profit_color}">Margin: {bi_metrics['profit_margin']:.1f}%</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">🛒 Total Orders</div>
        <div class="metric-value">{bi_metrics['total_orders']:,}</div>
        <div class="metric-sub text-blue">Avg Basket: ${bi_metrics['avg_order_val']:,.0f}</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    loss_color = "text-red" if bi_metrics['loss_percentage'] > 15 else "text-amber"
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">🚨 Unprofitable Orders</div>
        <div class="metric-value ${loss_color}">{bi_metrics['loss_percentage']:.1f}%</div>
        <div class="metric-sub ${loss_color}">Loss Amt: ${bi_metrics['total_loss_amount']:,.0f}</div>
    </div>
    """, unsafe_allow_html=True)

with col5:
    avg_disc = df_filtered['Discount'].mean() * 100 if not df_filtered.empty else 0
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">🏷️ Avg Discount Rate</div>
        <div class="metric-value text-amber">{avg_disc:.1f}%</div>
        <div class="metric-sub text-amber">Cross-Category Avg</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# 6. Dashboard Tabs
tab_insights, tab_trends, tab_category, tab_discount, tab_customer, tab_data = st.tabs([
    "💡 Executive Insights",
    "📊 Sales & Profit Trends",
    "📦 Category & Product Matrix",
    "🚨 Discount Optimization",
    "👥 Customer & Regional",
    "📋 Data Explorer"
])

# TAB 1: EXECUTIVE INSIGHTS
with tab_insights:
    st.subheader("🤖 Automated Business Intelligence Executive Insights")
    
    col_a, col_b = st.columns([3, 2])
    
    with col_a:
        st.markdown("#### Key Key Performance Observations")
        for item in bi_metrics['insights']:
            st.markdown(f"""
            <div class="insight-card {item['type']}">
                <strong style="font-size: 1.05rem;">{item['title']}</strong><br>
                <span style="color: #cbd5e1;">{item['text']}</span>
            </div>
            """, unsafe_allow_html=True)
            
    with col_b:
        st.markdown("#### 🎯 Strategic Data Analyst Recommendations")
        for rec in bi_metrics['recommendations']:
            st.info(rec)
            
        st.markdown("#### 📊 Metric Distribution Snapshot")
        if not df_filtered.empty:
            fig_pie = px.pie(
                df_filtered,
                names='Category',
                values='Sales',
                title="Revenue Share by Category",
                hole=0.4,
                color_discrete_sequence=px.colors.qualitative.Dark24
            )
            fig_pie.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color="#e0e6ed")
            st.plotly_chart(fig_pie, use_container_width=True)

# TAB 2: TRENDS
with tab_trends:
    st.subheader("📈 Revenue & Profit Dynamics Over Time")
    
    if not df_filtered.empty:
        # Monthly Aggregation
        monthly_df = df_filtered.groupby('Order_Year_Month').agg(
            Sales=('Sales', 'sum'),
            Profit=('Profit', 'sum')
        ).reset_index()
        
        fig_trend = go.Figure()
        fig_trend.add_trace(go.Scatter(
            x=monthly_df['Order_Year_Month'], y=monthly_df['Sales'],
            name="Revenue ($)", line=dict(color="#3b82f6", width=3), mode='lines+markers'
        ))
        fig_trend.add_trace(go.Scatter(
            x=monthly_df['Order_Year_Month'], y=monthly_df['Profit'],
            name="Net Profit ($)", line=dict(color="#10b981", width=3), mode='lines+markers'
        ))
        
        fig_trend.update_layout(
            title="Monthly Sales vs Net Profit Trend",
            xaxis_title="Year-Month",
            yaxis_title="Amount ($)",
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font_color="#e0e6ed",
            hovermode="x unified"
        )
        st.plotly_chart(fig_trend, use_container_width=True)
        
        col_t1, col_t2 = st.columns(2)
        with col_t1:
            # Regional Trend
            reg_df = df_filtered.groupby(['Region', 'Order_Year']).agg(Sales=('Sales', 'sum')).reset_index()
            fig_reg = px.bar(
                reg_df, x='Order_Year', y='Sales', color='Region',
                barmode='group', title="Yearly Revenue by Region"
            )
            fig_reg.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color="#e0e6ed")
            st.plotly_chart(fig_reg, use_container_width=True)
            
        with col_t2:
            # Shipping Days distribution
            fig_ship = px.histogram(
                df_filtered, x='Shipping_Days', color='Ship Mode',
                title="Delivery Duration Distribution (Days)",
                nbins=10
            )
            fig_ship.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color="#e0e6ed")
            st.plotly_chart(fig_ship, use_container_width=True)

# TAB 3: CATEGORY & PRODUCT MATRIX
with tab_category:
    st.subheader("📦 Product & Category Profitability Breakdown")
    
    if not df_filtered.empty:
        col_c1, col_c2 = st.columns(2)
        
        with col_c1:
            subcat_agg = df_filtered.groupby('Sub-Category').agg(
                Sales=('Sales', 'sum'),
                Profit=('Profit', 'sum')
            ).reset_index().sort_values(by='Profit', ascending=True)
            
            fig_sub = px.bar(
                subcat_agg, y='Sub-Category', x='Profit',
                orientation='h', color='Profit',
                color_continuous_scale=px.colors.diverging.Tealrose,
                title="Net Profit by Sub-Category"
            )
            fig_sub.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color="#e0e6ed")
            st.plotly_chart(fig_sub, use_container_width=True)
            
        with col_c2:
            prod_top = df_filtered.groupby('Product Name').agg(
                Sales=('Sales', 'sum'),
                Profit=('Profit', 'sum')
            ).reset_index().sort_values(by='Profit', ascending=False)
            
            st.markdown("#### 🏆 Top 5 Most Profitable Products")
            st.dataframe(prod_top.head(5).style.format({'Sales': '${:,.2f}', 'Profit': '${:,.2f}'}), use_container_width=True)
            
            st.markdown("#### ⚠️ Top 5 Loss-Making Products")
            st.dataframe(prod_top.tail(5).sort_values(by='Profit').style.format({'Sales': '${:,.2f}', 'Profit': '${:,.2f}'}), use_container_width=True)

# TAB 4: DISCOUNT OPTIMIZATION MATRIX
with tab_discount:
    st.subheader("🚨 Discount vs Profitability Leakage Analysis")
    st.markdown("""
    **Data Analyst Insight**: High discounts are often given to drive sales volume, but when discounts exceed **20-30%**, profit margins frequently drop below zero, creating invisible revenue leakage.
    """)
    
    if not df_filtered.empty:
        fig_scatter = px.scatter(
            df_filtered,
            x='Discount',
            y='Profit_Margin',
            color='Category',
            size='Sales',
            hover_data=['Sub-Category', 'Sales', 'Profit'],
            title="Discount Rate vs Profit Margin (%)",
            labels={'Discount': 'Discount Rate (0.1 = 10%)', 'Profit_Margin': 'Profit Margin (%)'}
        )
        fig_scatter.add_hline(y=0, line_dash="dash", line_color="red", annotation_text="Break-even line (0% Margin)")
        fig_scatter.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color="#e0e6ed")
        st.plotly_chart(fig_scatter, use_container_width=True)
        
        # Discount Group Summary Table
        disc_summary = df_filtered.groupby('Discount_Category', observed=False).agg(
            Order_Count=('Row ID', 'count'),
            Total_Sales=('Sales', 'sum'),
            Total_Profit=('Profit', 'sum'),
            Avg_Margin=('Profit_Margin', 'mean')
        ).reset_index()
        
        st.markdown("#### 📊 Profitability Matrix by Discount Tier")
        st.dataframe(disc_summary.style.format({
            'Total_Sales': '${:,.2f}',
            'Total_Profit': '${:,.2f}',
            'Avg_Margin': '{:.2f}%'
        }), use_container_width=True)

# TAB 5: CUSTOMER & REGIONAL
with tab_customer:
    st.subheader("👥 Customer Segment & Regional Distribution")
    
    if not df_filtered.empty:
        col_m1, col_m2 = st.columns(2)
        
        with col_m1:
            seg_df = df_filtered.groupby('Segment').agg(
                Sales=('Sales', 'sum'),
                Profit=('Profit', 'sum')
            ).reset_index()
            
            fig_seg = px.bar(
                seg_df, x='Segment', y=['Sales', 'Profit'],
                barmode='group', title="Sales vs Profit by Customer Segment",
                color_discrete_map={'Sales': '#3b82f6', 'Profit': '#10b981'}
            )
            fig_seg.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color="#e0e6ed")
            st.plotly_chart(fig_seg, use_container_width=True)
            
        with col_m2:
            state_df = df_filtered.groupby('State/Province').agg(
                Profit=('Profit', 'sum'),
                Sales=('Sales', 'sum')
            ).reset_index().sort_values(by='Sales', ascending=False).head(10)
            
            fig_state = px.bar(
                state_df, x='Sales', y='State/Province', orientation='h',
                color='Profit', title="Top 10 States by Sales & Profitability"
            )
            fig_state.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color="#e0e6ed")
            st.plotly_chart(fig_state, use_container_width=True)

# TAB 6: DATA EXPLORER & EXPORT
with tab_data:
    st.subheader("📋 Filtered Dataset Explorer")
    st.markdown(f"Displaying **{len(df_filtered):,}** records matching current sidebar filter selection.")
    
    st.dataframe(df_filtered, use_container_width=True, height=400)
    
    # Download Button
    csv = df_filtered.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Download Filtered Data as CSV",
        data=csv,
        file_name="superstore_filtered_data.csv",
        mime="text/csv"
    )
