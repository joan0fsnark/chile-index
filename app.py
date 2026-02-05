import streamlit as st
import pandas as pd
import re
import os

# --- Page Configuration ---
st.set_page_config(page_title="Chile Index Explorer", layout="wide", page_icon="🌶️")

st.title("🌶️ Chile Index Explorer")
st.write("An interactive guide to the botanical world of chile peppers.")

# --- Helper Functions for Data Sanitization ---

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

# --- Data Loading & Pipeline ---

@st.cache_data
def load_and_clean_data():
    if not os.path.exists("chile_data.csv"):
        return pd.DataFrame()
    try:
        df = pd.read_csv("chile_data.csv", engine='python', quotechar='"')
        
        # 1. Apply Sanitization
        df['Research-Accepted SHU'] = df['Research-Accepted SHU'].apply(clean_shu)
        df['0/10'] = df['0/10'].apply(sanitize_heat_score)
        df['Species'] = df['Species'].fillna('Unknown')
        df['Varietal'] = df['Varietal'].fillna('Other')
        df['Notes'] = df['Notes'].fillna('')

        # 2. DEFAULT ALPHABETICAL SORTING
        df = df.sort_values(by='Cultivar', ascending=True).reset_index(drop=True)
        
        return df
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return pd.DataFrame()

df = load_and_clean_data()

if not df.empty:
    # --- Sidebar Filters ---
    st.sidebar.header("Search & Filters")
    
    # SEARCH WITH AUTOCOMPLETE (Matches as you type)
    all_cultivars = ["All Varieties"] + df['Cultivar'].tolist()
    search_choice = st.sidebar.selectbox(
        "Search & Match Variety:", 
        options=all_cultivars,
        help="Type to find a specific pepper. The list is organized alphabetically."
    )

    # Multiselect Dropdowns
    all_species = sorted(df['Species'].unique().tolist())
    selected_species = st.sidebar.multiselect(
        "Scientific Species (*Italicized*):", 
        options=all_species, 
        default=None,
        placeholder="Filter by species..."
    )

    heat_range = st.sidebar.slider("Heat Intensity (0-10 Score):", 0.0, 10.0, (0.0, 10.0))

    # --- Filtering Logic ---
    mask = (df['0/10'].between(heat_range[0], heat_range[1]))

    if search_choice != "All Varieties":
        mask = mask & (df['Cultivar'] == search_choice)

    if selected_species:
        mask = mask & (df['Species'].isin(selected_species))
    
    filtered_df = df[mask].copy()

    # --- Metrics & Table ---
    c1, c2 = st.columns(2)
    c1.metric("Varieties Found", len(filtered_df))
    hottest_val = filtered_df['Research-Accepted SHU'].max()
    c2.metric("Hottest SHU", f"{int(hottest_val):,}" if not pd.isna(hottest_val) else "0")

    st.markdown("---")
    
    st.dataframe(
        filtered_df,
        column_config={
            "Cultivar": st.column_config.TextColumn("Variety Name"),
            "Species": st.column_config.TextColumn("Scientific Name (*Italics*)"),
            "Research-Accepted SHU": st.column_config.NumberColumn("Scoville (SHU)", format="%d"),
            "0/10": st.column_config.NumberColumn("Heat Score", format="%.1f"),
            "Notes": st.column_config.TextColumn("Notes", width="large")
        },
        width="stretch", 
        hide_index=True
    )
    
    # --- Sidebar Footer ---
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 📜 Credits & Licensing")
    st.sidebar.info(
        """
        **Data Architect:** u/BennyTheAstronaut  

        **Formula:** Collins et al. (1995) / ASTA  

        **License:** CC BY-NC 4.0
        """
    )

else:
    st.warning("Please ensure 'chile_data.csv' is in the same directory.")