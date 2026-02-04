import streamlit as st
import pandas as pd
import re

st.set_page_config(page_title="Chili Scoville Explorer", layout="wide")
st.title("🌶️ Interactive Chili Scoville Index")

def sanitize_heat_score(val):
    """
    The ultimate fix for the '<' error. 
    Converts dates, strings, and formatted text into clean floats.
    """
    s = str(val).strip().lower()
    
    # 1. Handle Excel Date Bug: '2026-02-10' -> 2.0
    if '-' in s:
        try:
            # Extract the month/day that represents the score
            parts = s.split('-')
            return float(parts[1]) if len(parts) > 1 else 0.0
        except: return 0.0
        
    # 2. Strip '/10' and '+' signs
    s = re.sub(r'/[0-9]+', '', s)
    s = s.replace('+', '')
    
    # 3. Final Conversion
    try:
        return float(s)
    except ValueError:
        return 0.0

try:
    # 1. Load Data
    df = pd.read_csv("chile_data.csv", engine='python', quotechar='"')

    # 2. SANITIZE IMMEDIATELY
    # This ensures the filtering logic never sees a 'str'
    df['0/10'] = df['0/10'].apply(sanitize_heat_score)
    df['Research-Accepted SHU'] = pd.to_numeric(df['Research-Accepted SHU'], errors='coerce').fillna(0)

    # --- Sidebar Filters ---
    st.sidebar.header("Search & Filters")
    search_query = st.sidebar.text_input("Search Variety or Keyword:")

    # Get unique species and varietals for the dropdowns
    all_species = sorted(df['Species'].dropna().unique())
    selected_species = st.sidebar.multiselect("Species:", all_species, default=all_species)

    all_varietals = sorted(df['Varietal'].dropna().unique())
    selected_varietals = st.sidebar.multiselect("Varietal:", all_varietals, default=all_varietals)

    # Slider now works with guaranteed floats
    heat_range = st.sidebar.slider("Heat Intensity (0-10):", 0.0, 10.0, (0.0, 10.0))

    # --- Filtering Logic ---
    mask = (
        df['Species'].isin(selected_species) &
        df['Varietal'].isin(selected_varietals) &
        df['0/10'].between(heat_range[0], heat_range[1])
    )
    
    filtered_df = df[mask].copy()

    # Search feature
    if search_query:
        filtered_df = filtered_df[
            filtered_df['Cultivar'].str.contains(search_query, case=False, na=False) |
            filtered_df['Notes'].str.contains(search_query, case=False, na=False)
        ]

    # --- Dashboard Metrics ---
    if not filtered_df.empty:
        c1, c2, c3 = st.columns(3)
        c1.metric("Varieties", len(filtered_df))
        c2.metric("Hottest SHU", f"{int(filtered_df['Research-Accepted SHU'].max()):,}")
        c3.metric("Species Count", filtered_df['Species'].nunique())

# --- Data Table ---
        st.markdown("### Pepper Varieties")
        st.dataframe(
            filtered_df,
            column_config={
                "Cultivar": st.column_config.TextColumn("Variety Name"),
                "Species": st.column_config.TextColumn("Scientific Name"),
                "Research-Accepted SHU": st.column_config.NumberColumn("Scoville (SHU)", format="%d"),
                "0/10": st.column_config.NumberColumn("Heat Score", format="%.1f"),
                "Notes": st.column_config.TextColumn("Notes")
            },
            width="stretch", # Replaces use_container_width=True
            hide_index=True
        )
    else:
        st.warning("No matches found for those filters.")

except Exception as e:
    st.error(f"Unexpected Error: {e}")