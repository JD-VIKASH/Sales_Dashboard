# 📊 Superstore Sales & Business Intelligence Analytics Dashboard

![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.56-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)
![Plotly](https://img.shields.io/badge/Plotly-6.9-3F4F75?style=for-the-badge&logo=plotly&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-3.0-150458?style=for-the-badge&logo=pandas&logoColor=white)

An executive-grade **Business Intelligence & Sales Analytics Dashboard** built for data analysts, business managers, and decision-makers to track revenue performance, net profit margins, customer segment behavior, regional trends, and discount profit leakage.

---

## 🚀 Live Dashboard Preview

Run locally in one command:
```bash
streamlit run main.py
```
Access in your browser at: **`http://localhost:8501`**

---

## 🎯 Key Business Intelligence Features

### 1. 💡 Executive BI Insights Engine
- **Automated Performance Highlights**: Color-coded cards indicating financial health (Green = Healthy, Yellow = Moderate, Red = Alert).
- **Strategic Recommendations**: Actionable insights automatically generated based on active filters (e.g., discount capping on loss-making categories).

### 2. 📊 Revenue & Profit Dynamics
- **Monthly Time-Series Trends**: Interactive dual-axis line charts tracking Sales vs Net Profit over time.
- **Delivery Duration**: Delivery turnaround time histograms grouped by shipping mode (*Standard*, *Second Class*, *First Class*, *Same Day*).

### 3. 📦 Category & Product Matrix
- **Sub-Category Profitability**: Horizontal bar charts identifying high-margin vs low-margin sub-categories.
- **Top 5 & Bottom 5 Products**: Tabular rankings of top profitable products vs top profit-draining items.

### 4. 🚨 Discount Optimization Matrix
- **Break-Even Analysis**: Scatter plot matrix comparing Discount Rate vs Profit Margin with an explicit break-even line ($y=0$).
- **Profit Leakage Warning**: Multi-tier breakdown highlighting how heavy discounts ($\ge 30\%$) destroy bottom-line profitability.

### 5. 👥 Customer Segment & Regional Analytics
- **Segment Breakdown**: Grouped bar charts comparing Sales vs Net Profit across *Consumer*, *Corporate*, and *Home Office*.
- **Geographic Performance**: State-level revenue and profit ranking for top performing territories.

### 6. 📋 Data Explorer & Export
- Searchable data table with instant dynamic filtering.
- One-click **CSV Export** button for downstream reporting.

---

## 📂 Project Architecture

```
DataAnalyst1/
│
├── data/
│   ├── raw/
│   │   └── sample_-_superstore.xls       # Raw Superstore Excel dataset
│   └── clean/
│       └── superstore_cleaned.csv        # Cleaned & feature-engineered dataset
│
├── notebook/
│   └── 01_data_exploration.ipynb         # Exploratory Data Analysis (EDA) notebook
│
├── scripts/
│   └── clean_data.py                     # Data cleaning & transformation pipeline
│
├── src/
│   ├── __init__.py
│   ├── data_loader.py                    # Cached data loader & dynamic filter module
│   └── insights.py                       # Automated BI Insights generator engine
│
├── .gitignore                            # Excluded files & directories
├── main.py                               # Main Streamlit BI Dashboard application
├── query.sql                             # SQL queries for database integration
├── requirements.txt                      # Project python dependencies
└── README.md                             # Project documentation
```

---

## 📈 Key Findings & Executive Insights

1. **Overall Performance**: Generated **$2.33M** in total revenue with **$292.3K** net profit (**12.56%** net margin).
2. **Profit Leakage Alert**: **18.6%** of transactions operate at a net loss, accumulating **$157,039** in negative profit.
3. **Discount Threshold Warning**: Discounts over **20-30%** create immediate profit loss (especially in *Tables* and *Bookcases*).
4. **Category Champions**: *Technology* delivers the highest profit margin, whereas promotional discounts in *Furniture* heavily drag overall profit down.

---

## 🛠️ Installation & Quick Setup

### 1. Clone the Repository
```bash
git clone https://github.com/JD-VIKASH/Sales_Dashboard.git
cd Sales_Dashboard
```

### 2. Create Virtual Environment (Optional but Recommended)
```bash
python -m venv .venv
source .venv/bin/activate    # On Linux/macOS
.venv\Scripts\activate       # On Windows
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the Data Pipeline (If modifying raw data)
```bash
python scripts/clean_data.py
```

### 5. Launch the Dashboard
```bash
streamlit run main.py
```

---

## 👤 Author
Developed by **JD-VIKASH**  
GitHub Repository: [JD-VIKASH/Sales_Dashboard](https://github.com/JD-VIKASH/Sales_Dashboard)
