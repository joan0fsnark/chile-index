import streamlit as st
import pandas as pd
import re
import os

# --- Page Config ---
st.set_page_config(page_title="Chile Index Explorer", layout="wide", page_icon="🌶️")

st.title("🌶️ Chile Index Explorer")

# --- Cleaning Functions ---
def clean_shu(val):
    if pd.isna(val): return 0.0
    s = str(val).replace(',', '').strip().lower()
    if '-' in s:
        try:
            parts = [float(p.strip()) for p in s.split('-') if p.strip().replace('.','',1).isdigit()]
            return sum(parts) / len(parts) if parts else 0.0
        except: return 0.0
    try:
        numeric_part = ''.join(filter(lambda x: x.isdigit() or x == '.', s))
        return float(numeric_part) if numeric_part else 0.0
    except: return 0.0

def sanitize_heat_score(val):
    if pd.isna(val): return 0.0
    s = str(val).strip().lower()
    if '-' in s:
        try:
            parts = s.split('-')
            return float(parts[1]) if len(parts) > 1 else 0.0
        except: return 0.0
    s = re.sub(r'/[0-9]+', '', s).replace('+', '')
    try: return float(s)
    except: return 0.0

# --- Data Loading ---
if not os.path.exists("chile_data.csv"):
    st.error("❌ 'chile_data.csv' not found in current directory!")
    st.info(f"Current Directory: {os.getcwd()}")
    st.stop()

try:
    df = pd.read_csv("chile_data.csv", engine='python', quotechar='"')
    
    # Clean data immediately
    df['Research-Accepted SHU'] = df['Research-Accepted SHU'].apply(clean_shu)
    df['0/10'] = df['0/10'].apply(sanitize_heat_score)
    df['Species'] = df['Species'].fillna('Unknown')
    df['Varietal'] = df['Varietal'].fillna('Other')
    
    # --- Sidebar ---
    st.sidebar.header("Filters")
    search = st.sidebar.text_input("Search Variety/Notes:")
    
    # Use lists for multiselect
    spec_list = sorted(df['Species'].unique().tolist())
    sel_spec = st.sidebar.multiselect("Species:", spec_list, default=spec_list)
    
    var_list = sorted(df['Varietal'].unique().tolist())
    sel_var = st.sidebar.multiselect("Varietal:", var_list, default=var_list)
    
    heat_range = st.sidebar.slider("Heat Score (0-10):", 0.0, 10.0, (0.0, 10.0))

    # --- Filter ---
    mask = (
        df['Species'].isin(sel_spec) & 
        df['Varietal'].isin(sel_var) & 
        df['0/10'].between(heat_range[0], heat_range[1])
    )
    
    f_df = df[mask].copy()
    if search:
        f_df = f_df[f_df['Cultivar'].str.contains(search, case=False, na=False) | 
                    f_df['Notes'].str.contains(search, case=False, na=False)]

    # --- Display ---
    m1, m2 = st.columns(2)
    m1.metric("Varieties", len(f_df))
    m2.metric("Max Heat (SHU)", f"{int(f_df['Research-Accepted SHU'].max()):,}")

    st.dataframe(
        f_df,
        column_config={
            "Research-Accepted SHU": st.column_config.NumberColumn("Scoville", format="%d"),
            "0/10": st.column_config.NumberColumn("Score", format="%.1f")
        },
        width="stretch",
        hide_index=True
    )

except Exception as e:
    st.error(f"Critical Error: {e}")

    # --- Credits & Sources ---
st.sidebar.markdown("---")
st.sidebar.markdown("### 📜 Credits")
st.sidebar.info(
    """
    **Data Source:** Curated by **[u/BennyTheAstronaut](https://www.reddit.com/user/BennyTheAstronaut/)**.  
    
    **Research Reference:** SHU calculation formulas based on *Collins et al. (1995)*.
    """
)