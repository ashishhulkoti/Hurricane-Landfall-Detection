import streamlit as st
import pandas as pd
from src.parser import parse_hurdat2
from src.geoutil import load_state_polygon
from src.detector import detect_landfalls_by_path, detect_landfalls_by_indicator
import folium
from streamlit_folium import st_folium

# --- PAGE SETUP ---
st.set_page_config(page_title="HURDAT2 Landfall Detection", layout="wide")
st.title("🌀 HURDAT2 Florida Landfall Detector")

hurdat_path = "data/hurdat2.txt"
shapefile_path = "shapefiles/tl_2025_us_state/tl_2025_us_state.shp"


# --- HELPER: PLOT MAP ---
def create_map(df, color="red"):
    m = folium.Map(location=[27.5, -83.0], zoom_start=6)
    for _, row in df.iterrows():
        folium.CircleMarker(
            location=[row["lat"], row["lon"]],
            radius=3,
            color=color,
            fill=True,
            fill_opacity=0.7,
            popup=f"{row['name']} ({row['wind']} kt)"
        ).add_to(m)
    return m

# --- LOAD POLYGON ONCE ---
try:
    if "state_polygon" not in st.session_state:
        st.session_state.state_polygon = load_state_polygon(shapefile_path, 'Florida')
except Exception as e:
    st.error(f"❌ Error loading shapefile: {e}")
    st.stop()



# --- INTRO ---
st.markdown("""
This dashboard analyzes NOAA’s HURDAT2 dataset to detect **hurricane landfalls in Florida**.

- **Method A** detects landfalls *algorithmically* by analyzing storm paths.  
- **Method B** detects landfalls using the official NOAA **'L' indicator**.  
Results are visualized below and can be downloaded as CSV files.
""")



# --- METHOD A ---
if st.button("Run Landfall Detection (Method A – Path-Based)", key="btn_method_a"):
    with st.spinner("Parsing and detecting landfalls (Method A)..."):
        df = parse_hurdat2(hurdat_path).sort_values(by='datetime')
        st.session_state.results_a = detect_landfalls_by_path(df, st.session_state.state_polygon)
        st.session_state.method_a_done = True  # ✅ do NOT reset method_b_done here

# --- METHOD B ---
if st.button("Run Landfall Detection (Method B – Indicator L)", key="btn_method_b"):
    with st.spinner("Parsing and detecting landfalls (Method B)..."):
        df = parse_hurdat2(hurdat_path).sort_values(by='datetime')
        st.session_state.results_b = detect_landfalls_by_indicator(df, st.session_state.state_polygon)
        st.session_state.method_b_done = True  # ✅ do NOT reset method_a_done here


# --- SHOW RESULTS AFTER BUTTON CLICK ---
if st.session_state.get("method_a_done", False):
    results_a = st.session_state.results_a
    st.success(f"✅ Found {len(results_a)} landfalls using Method A")
    st.dataframe(results_a)
    st.download_button("Download Method A CSV",
                       results_a.to_csv(index=False),
                       "landfalls_method_a.csv")
    st.subheader("🌍 Map: Method A Landfall Points")
    st_folium(create_map(results_a, color="blue"), width=700, height=500, key="method_a_main_map")

if st.session_state.get("method_b_done", False):
    results_b = st.session_state.results_b
    st.success(f"✅ Found {len(results_b)} landfalls using Method B")
    st.dataframe(results_b)
    st.download_button("Download Method B CSV",
                       results_b.to_csv(index=False),
                       "landfalls_method_b.csv")
    st.subheader("🌍 Map: Method B Landfall Points")
    st_folium(create_map(results_b, color="red"), width=700, height=500, key="method_b_main_map")


# --- COMPARISON SECTION ---
if st.session_state.get("method_a_done") and st.session_state.get("method_b_done"):
    st.subheader("📊 Comparison of Method A vs Method B")

    results_a = st.session_state.results_a
    results_b = st.session_state.results_b

    a, b = len(results_a), len(results_b)
    st.info(f"**Method A:** {a} landfalls  |  **Method B:** {b} landfalls")

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Method A Map")
        st_folium(create_map(results_a, color="blue"), width=350, height=400, key="method_a_compare_map")
    with col2:
        st.subheader("Method B Map")
        st_folium(create_map(results_b, color="red"), width=350, height=400, key="method_b_compare_map")


# if st.button("🔄 Reset"):
#     for key in ["results_a", "results_b", "method_a_done", "method_b_done"]:
#         if key in st.session_state:
#             del st.session_state[key]
#     st.experimental_rerun()



st.markdown("<hr>", unsafe_allow_html=True)
st.caption("HURDAT2 Florida Landfall Detector — developed by Ashish Hulkoti © 2025")
