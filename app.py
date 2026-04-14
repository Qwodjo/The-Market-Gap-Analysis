import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Page Configuration
st.set_page_config(
    page_title="Sugar Trap — Market Gap Analysis",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling (CSS)
st.markdown("""
    <style>
    /* Global Fixes */
    footer { visibility: hidden; }

    /* Responsive container */
    .main .block-container {
        padding-top: 2rem !important;
        max-width: 90% !important; 
    }

    /* Sidebar Theme Setup */
    section[data-testid="stSidebar"] {
        background-color: var(--secondary-background-color) !important;
        border-right: 1px solid rgba(128,128,128,0.2) !important;
    }
    section[data-testid="stSidebar"] [data-testid="stVerticalBlock"] {
        background-color: var(--secondary-background-color) !important;
    }

    /* Typography & Core Elements */
    .main-heading {
        font-size: 42px;
        font-weight: 900;
        color: var(--text-color);
        text-align: center;
        letter-spacing: 2px;
        margin-bottom: 28px;
        text-transform: uppercase;
        font-family: Arial, sans-serif;
    }
    .section-header {
        font-size: 20px;
        font-weight: 800;
        color: var(--text-color);
        margin: 32px 0 14px 0;
        padding-bottom: 10px;
        border-bottom: 2px solid rgba(128,128,128,0.2);
        letter-spacing: 0.2px;
        font-family: Arial, sans-serif;
    }

    /* KPI Cards */
    .kpi-card {
        background: var(--background-color);
        border-radius: 12px;
        border: 1px solid rgba(128,128,128,0.2);
        padding: 16px 20px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.06);
        transition: all 0.2s ease;
        height: 100%;
    }
    .kpi-card:hover {
        box-shadow: 0 6px 16px rgba(0,0,0,0.12);
        transform: translateY(-2px);
    }
    .kpi-gradient-line {
        height: 3px;
        border-radius: 2px;
        margin-bottom: 12px;
    }
    .kpi-label {
        font-size: 10px;
        font-weight: 600;
        color: var(--text-color);
        opacity: 0.6;
        letter-spacing: 1px;
        text-transform: uppercase;
        margin-bottom: 8px;
        font-family: Arial, sans-serif;
    }
    .kpi-value {
        font-size: 28px;
        font-weight: 800;
        color: var(--text-color);
        margin-bottom: 4px;
        line-height: 1;
        font-family: Arial, sans-serif;
    }
    .kpi-sub {
        font-size: 11px;
        color: var(--text-color);
        opacity: 0.6;
        font-weight: 500;
        font-family: Arial, sans-serif;
    }

    /* Insights & Recommendations */
    .insight-box {
        background: var(--background-color);
        border: 1px solid rgba(128,128,128,0.2);
        border-radius: 10px;
        padding: 24px 28px;
        margin: 12px 0;
        line-height: 2;
        color: var(--text-color);
        font-size: 14px;
        font-family: Arial, sans-serif;
    }
    .insight-heading {
        color: var(--text-color);
        font-size: 15px;
        font-weight: 900;
        display: block;
        margin-bottom: 14px;
        font-family: Arial, sans-serif;
    }

    /* Protein Analysis Cards */
    .protein-card {
        background: var(--background-color);
        border: 1px solid rgba(128,128,128,0.2);
        border-radius: 10px;
        padding: 28px 20px;
        text-align: center;
        box-shadow: 0 2px 6px rgba(0,0,0,0.06);
        transition: all 0.2s ease;
    }
    .protein-card:hover {
        box-shadow: 0 6px 16px rgba(0,0,0,0.12);
        transform: translateY(-2px);
    }
    .protein-rank {
        font-size: 11px;
        color: var(--text-color);
        opacity: 0.6;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 10px;
        font-weight: 600;
        font-family: Arial, sans-serif;
    }
    .protein-name {
        font-size: 28px;
        font-weight: 900;
        color: var(--text-color);
        margin-bottom: 8px;
        font-family: Arial, sans-serif;
    }
    .protein-pct {
        font-size: 16px;
        color: var(--text-color);
        font-weight: 900;
        margin-bottom: 6px;
        font-family: Arial, sans-serif;
    }
    .protein-count {
        font-size: 12px;
        color: var(--text-color);
        opacity: 0.5;
        font-family: Arial, sans-serif;
    }

    /* Sidebar Elements */
    section[data-testid="stSidebar"] input[type="checkbox"] {
        accent-color: #3939f7 !important;
    }
    section[data-testid="stSidebar"] h3,
    section[data-testid="stSidebar"] .sidebar-filters-heading {
        color: #3939f7 !important;
        font-weight: 900 !important;
    }
    .sidebar-count {
        background: rgba(37,99,235,0.08);
        border: 1px solid rgba(37,99,235,0.2);
        border-radius: 8px;
        padding: 12px 16px;
        margin-top: 12px;
        font-family: Arial, sans-serif;
    }
    .sidebar-count-value {
        font-size: 20px;
        font-weight: 800;
        color: var(--text-color);
        font-family: Arial, sans-serif;
    }
    .sidebar-count-label {
        font-size: 11px;
        color: var(--text-color);
        opacity: 0.6;
        font-family: Arial, sans-serif;
    }

    /* Footer */
    .dashboard-footer {
        text-align: center;
        padding: 24px 0 12px 0;
        color: var(--text-color);
        opacity: 0.6;
        font-size: 13px;
        border-top: 1px solid rgba(128,128,128,0.2);
        margin-top: 48px;
        font-weight: 500;
        font-family: Arial, sans-serif;
    }
    </style>
""", unsafe_allow_html=True)

# Data Loading & Initialization
SHEET_ID = "1FzOe2FoWMU92MZVqhodN-CLRFRdwadbo2PGHGPlUREw"
URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv"

@st.cache_data
def load_data():
    return pd.read_csv(URL)

df = load_data()

# Plotly Global Theme Rules
plotly_theme = dict(
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)',
    font=dict(family='Arial'),
    xaxis=dict(
        gridcolor='rgba(128,128,128,0.2)',
        linecolor='rgba(128,128,128,0.2)'
    ),
    yaxis=dict(
        gridcolor='rgba(128,128,128,0.2)',
        linecolor='rgba(128,128,128,0.2)'
    ),
    legend=dict(
        bgcolor='rgba(0,0,0,0)',
        bordercolor='rgba(128,128,128,0.2)',
        borderwidth=1
    )
)

category_colors = {
    'Cookies & Biscuits': '#E74C3C',
    'Chips & Crisps': '#E67E22',
    'Chocolate & Candy': '#8E44AD',
    'Protein & Nutrition Bars': '#27AE60',
    'Cereals & Breakfast': '#F39C12',
    'Nuts & Seeds': '#2E86C1',
    'Dairy Snacks': '#17A589',
}

# Sidebar Controls
st.sidebar.markdown(
    "<p style='font-size:16px; font-weight:900; color:#6B7280; "
    "letter-spacing:1px; margin: 8px 0 16px 0; font-family:Arial;'>"
    "FILTERS</p>",
    unsafe_allow_html=True
)

all_categories = sorted(df['primary_category'].unique().tolist())

# Manage Checkbox Session State for Selection Toggles
if 'cat_select_all' not in st.session_state:
    st.session_state['cat_select_all'] = True
for cat in all_categories:
    key = f"cat_{cat}"
    if key not in st.session_state:
        st.session_state[key] = True

st.sidebar.markdown(
    "<p style='font-size:10px; font-weight:600; color:#6B7280; "
    "letter-spacing:1.5px; text-transform:uppercase; margin-bottom:4px;'>"
    "CATEGORIES</p>",
    unsafe_allow_html=True
)

def toggle_all():
    new_val = st.session_state['cat_select_all']
    for cat in all_categories:
        st.session_state[f"cat_{cat}"] = new_val

st.sidebar.checkbox("Select All", key='cat_select_all', on_change=toggle_all)

selected_categories = []
for cat in all_categories:
    if st.sidebar.checkbox(cat, key=f"cat_{cat}"):
        selected_categories.append(cat)

if not selected_categories:
    selected_categories = all_categories

st.sidebar.markdown("<hr style='border-color:#E5E7EB; margin:14px 0;'>", unsafe_allow_html=True)

# Sugar Filters
st.sidebar.markdown(
    "<p style='font-size:10px; font-weight:600; color:#6B7280; "
    "letter-spacing:1.5px; text-transform:uppercase; margin-bottom:4px;'>"
    "SUGAR RANGE (g per 100g)</p>",
    unsafe_allow_html=True
)
scol1, scol2 = st.sidebar.columns(2)
with scol1:
    sugar_min = st.number_input("Min", min_value=0.0, value=0.0, step=0.1, format="%.1f", key="sugar_min")
with scol2:
    sugar_max = st.number_input("Max", min_value=0.0, value=100.0, step=0.1, format="%.1f", key="sugar_max")

st.sidebar.markdown("<hr style='border-color:#E5E7EB; margin:14px 0;'>", unsafe_allow_html=True)

# Protein Filters
st.sidebar.markdown(
    "<p style='font-size:10px; font-weight:600; color:#6B7280; "
    "letter-spacing:1.5px; text-transform:uppercase; margin-bottom:4px;'>"
    "PROTEIN RANGE (g per 100g)</p>",
    unsafe_allow_html=True
)
pcol1, pcol2 = st.sidebar.columns(2)
with pcol1:
    protein_min = st.number_input("Min", min_value=0.0, value=0.0, step=0.1, format="%.1f", key="protein_min")
with pcol2:
    protein_max = st.number_input("Max", min_value=0.0, value=100.0, step=0.1, format="%.1f", key="protein_max")

st.sidebar.markdown("<hr style='border-color:#E5E7EB; margin:14px 0;'>", unsafe_allow_html=True)

# Data Filtering
df_filtered = df[
    (df['primary_category'].isin(selected_categories)) &
    (df['sugars_100g'] >= sugar_min) &
    (df['sugars_100g'] <= sugar_max) &
    (df['proteins_100g'] >= protein_min) &
    (df['proteins_100g'] <= protein_max)
]

# # Sidebar Statistics
# st.sidebar.markdown(f"""
# <div class="sidebar-count">
#     <div class="sidebar-count-value">{len(df_filtered):,}</div>
#     <div class="sidebar-count-label">of {len(df):,} products showing</div>
# </div>
# """, unsafe_allow_html=True)


# Main Dashboard Layout
st.markdown("""
    <div class="main-heading">
        SUGAR TRAP — MARKET GAP ANALYSIS
    </div>
""", unsafe_allow_html=True)

# Key Performance Indicators (KPIs)
blue_ocean = df[(df['proteins_100g'] > 20) & (df['sugars_100g'] < 20)]
blue_ocean_pct = round((len(blue_ocean) / len(df)) * 100, 1)
protein_bars = df[df['primary_category'] == 'Protein & Nutrition Bars']
choc_candy = df[df['primary_category'] == 'Chocolate & Candy']
ratio = round(len(choc_candy) / len(protein_bars), 1)

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-gradient-line" style="background: linear-gradient(90deg, #f59e0b, #ef4444);"></div>
        <div class="kpi-label">Filtered Products</div>
        <div class="kpi-value">{len(df_filtered):,}</div>
        <div class="kpi-sub">of {len(df):,} total showing</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-gradient-line" style="background: linear-gradient(90deg, #06b6d4, #3b82f6);"></div>
        <div class="kpi-label">Total Products</div>
        <div class="kpi-value">{len(df):,}</div>
        <div class="kpi-sub">Products analyzed</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-gradient-line" style="background: linear-gradient(90deg, #10b981, #06b6d4);"></div>
        <div class="kpi-label">Categories</div>
        <div class="kpi-value">{df['primary_category'].nunique()}</div>
        <div class="kpi-sub">High level buckets</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-gradient-line" style="background: linear-gradient(90deg, #a78bfa, #ec4899);"></div>
        <div class="kpi-label">Blue Ocean Products</div>
        <div class="kpi-value">{blue_ocean_pct}%</div>
        <div class="kpi-sub">High Protein + Low Sugar</div>
    </div>
    """, unsafe_allow_html=True)

with col5:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-gradient-line" style="background: linear-gradient(90deg, #0ea5e9, #6366f1);"></div>
        <div class="kpi-label">Protein Bar Products</div>
        <div class="kpi-value">{len(protein_bars):,}</div>
        <div class="kpi-sub">{ratio}x fewer than Chocolates</div>
    </div>
    """, unsafe_allow_html=True)

# Nutrition Distribution Scatter Plot
st.markdown('<div class="section-header">Sugar vs Protein</div>', unsafe_allow_html=True)

fig_scatter = px.scatter(
    df_filtered,
    x='sugars_100g',
    y='proteins_100g',
    color='primary_category',
    color_discrete_map=category_colors,
    hover_name='product_name',
    hover_data={
        'sugars_100g': ':.1f',
        'proteins_100g': ':.1f',
        'primary_category': False
    },
    labels={
        'sugars_100g': 'Sugar per 100g (g)',
        'proteins_100g': 'Protein per 100g (g)',
        'primary_category': 'Category'
    },
    opacity=0.6,
)

fig_scatter.add_hline(y=20, line_dash='dash', line_color='#9CA3AF', line_width=1)
fig_scatter.add_vline(x=20, line_dash='dash', line_color='#9CA3AF', line_width=1)
fig_scatter.add_annotation(
    x=8, y=90,
    text='BLUE OCEAN<br>High Protein + Low Sugar',
    showarrow=False,
    font=dict(color='#1D4ED8', size=11, family='Arial'),
    bgcolor='rgba(239,246,255,0.95)',
    bordercolor='#BFDBFE',
    borderwidth=1,
    borderpad=10
)
fig_scatter.update_layout(
    **plotly_theme,
    height=520,
    xaxis_range=[0, 100],
    yaxis_range=[0, 100],
    legend_title=dict(text='Category'),
    margin=dict(l=20, r=20, t=20, b=40)
)
fig_scatter.update_xaxes(showgrid=True, gridcolor='rgba(128,128,128,0.2)')
fig_scatter.update_yaxes(showgrid=True, gridcolor='rgba(128,128,128,0.2)')
st.plotly_chart(fig_scatter, use_container_width=True)

# Health Score Analysis
st.markdown('<div class="section-header">Health Score By Category</div>', unsafe_allow_html=True)
st.markdown(
    "<p style='color:#6B7280; font-size:13px; margin-bottom:12px;'>"
    "Formula: Health Score = (Protein x 2) + (Fiber x 1.5) - (Sugar x 1) - (Fat x 0.5)</p>",
    unsafe_allow_html=True
)

health_by_category = df_filtered.groupby('primary_category')['health_score'].mean().round(1).reset_index()
health_by_category = health_by_category.sort_values('health_score', ascending=True)

bar_colors_health = ['#10B981' if score > 0 else '#EF4444' for score in health_by_category['health_score']]

x_max = round(health_by_category['health_score'].max() * 1.2)
x_min = round(health_by_category['health_score'].min() * 1.2)

fig_health = go.Figure(go.Bar(
    x=health_by_category['health_score'],
    y=health_by_category['primary_category'],
    orientation='h',
    marker_color=bar_colors_health,
    marker_line_width=0,
    text=health_by_category['health_score'],
    textposition='outside'
))
fig_health.add_vline(x=0, line_color='rgba(128,128,128,0.5)', line_width=1.5)
fig_health.update_layout(
    **plotly_theme,
    height=400,
    xaxis_range=[x_min, x_max],
    margin=dict(l=20, r=120, t=20, b=40)
)
st.plotly_chart(fig_health, use_container_width=True)

# Category Insights & Counts
st.markdown('<div class="section-header">Category Analysis</div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    category_avg = df_filtered.groupby('primary_category').agg(
        avg_sugar   = ('sugars_100g',   'mean'),
        avg_protein = ('proteins_100g', 'mean')
    ).round(1).reset_index()
    category_avg = category_avg.sort_values('avg_protein', ascending=False)

    fig_nutrition = go.Figure()
    fig_nutrition.add_trace(go.Bar(
        name='Average Sugar',
        x=category_avg['primary_category'],
        y=category_avg['avg_sugar'],
        marker_color='#EF4444',
        marker_line_width=0
    ))
    fig_nutrition.add_trace(go.Bar(
        name='Average Protein',
        x=category_avg['primary_category'],
        y=category_avg['avg_protein'],
        marker_color='#10B981',
        marker_line_width=0
    ))
    fig_nutrition.update_layout(
        **plotly_theme,
        title=dict(text='Average Sugar vs Protein By Category', font=dict(size=13)),
        barmode='group',
        height=420,
        margin=dict(l=20, r=20, t=40, b=100)
    )
    fig_nutrition.update_layout(
        legend=dict(
            orientation='h', y=-0.35, x=0.15,
            bgcolor='rgba(0,0,0,0)', bordercolor='rgba(128,128,128,0.2)', borderwidth=1
        )
    )
    fig_nutrition.update_xaxes(tickangle=-30)
    st.plotly_chart(fig_nutrition, use_container_width=True)

with col2:
    category_counts = df_filtered['primary_category'].value_counts().reset_index()
    category_counts.columns = ['primary_category', 'count']
    category_counts = category_counts.sort_values('count', ascending=True)

    bar_colors_count = [category_colors.get(cat, '#9CA3AF') for cat in category_counts['primary_category']]

    fig_count = go.Figure(go.Bar(
        x=category_counts['count'],
        y=category_counts['primary_category'],
        orientation='h',
        marker_color=bar_colors_count,
        marker_line_width=0,
        text=category_counts['count'],
        textposition='outside'
    ))
    fig_count.update_layout(
        **plotly_theme,
        title=dict(text='Number Of Products Per Category', font=dict(size=13)),
        height=420,
        margin=dict(l=20, r=100, t=40, b=40)
    )
    st.plotly_chart(fig_count, use_container_width=True)

# Strategy Insight Section
st.markdown('<div class="section-header">Key Insight & Product Recommendation</div>', unsafe_allow_html=True)

target_protein = round(protein_bars['proteins_100g'].median(), 1)
target_sugar = round(protein_bars['sugars_100g'].median(), 1)

st.markdown(f"""
<div class="insight-box">
    <span class="insight-heading">
        Based on the data the biggest market opportunity is in
        Protein & Nutrition Bars specifically targeting products
        with {target_protein}g of protein and less than {target_sugar}g of sugar.
    </span>
    Supporting Evidence:<br>
    &nbsp;&nbsp;— Only {len(protein_bars):,} products exist in the Protein & Nutrition Bars category<br>
    &nbsp;&nbsp;— Only {blue_ocean_pct}% of all analyzed products are in the Blue Ocean quadrant<br>
    &nbsp;&nbsp;— Chocolate & Candy has {ratio}x more products than Protein & Nutrition Bars<br>
    &nbsp;&nbsp;— Average Health Score of Protein Bars is 96.1 vs -34.7 for Chocolate & Candy
</div>
""", unsafe_allow_html=True)

# Top Protein Source Analysis
st.markdown('<div class="section-header">The Hidden Gem — Top Protein Sources</div>', unsafe_allow_html=True)
st.markdown(
    "<p style='color:#6B7280; font-size:13px; margin-bottom:16px;'>"
    "Analysis of ingredients in high protein low sugar products reveals the top protein sources.</p>",
    unsafe_allow_html=True
)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="protein-card">
        <div class="protein-rank">1st Most Common</div>
        <div class="protein-name">Milk</div>
        <div class="protein-pct">39.6%</div>
        <div class="protein-count">Found in 486 products</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="protein-card">
        <div class="protein-rank">2nd Most Common</div>
        <div class="protein-name">Peanut</div>
        <div class="protein-pct">23.2%</div>
        <div class="protein-count">Found in 285 products</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="protein-card">
        <div class="protein-rank">3rd Most Common</div>
        <div class="protein-name">Soy</div>
        <div class="protein-pct">14.5%</div>
        <div class="protein-count">Found in 178 products</div>
    </div>
    """, unsafe_allow_html=True)

# Dashboard Footer
st.markdown("""
<div class="dashboard-footer">
    Analysis by Enoch Kumi Asamoah, (2026)
</div>
""", unsafe_allow_html=True)