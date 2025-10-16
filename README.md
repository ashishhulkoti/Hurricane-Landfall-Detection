# 🌀 Florida Hurricane Landfall Detection

An interactive data analysis project that identifies **hurricane landfall events in Florida** using the  
**NOAA HURDAT2 “Best Track” Dataset** — the official historical record of Atlantic tropical cyclones.

The project combines data parsing, geospatial analysis, and visualization in an intuitive **Streamlit** dashboard.

---

## 🌍 Overview

This application parses NOAA’s HURDAT2 dataset (6.5 MB text file of storm tracks recorded every 6 hours)  
and detects when hurricanes made **landfall in Florida**.

Two independent methods are implemented and compared:

| Method | Description |
|---------|--------------|
| **Method A – Path-Based Detection** | Identifies landfall when a storm’s track crosses from ocean into Florida’s geographic boundary (using shapefiles and geometric containment checks). |
| **Method B – Indicator-Based Detection** | Uses NOAA’s built-in `L` flag within HURDAT2 that marks observed landfall points. |

Both results can be explored interactively on maps, compared side-by-side, and exported as CSV reports.

---

## 🧠 Project Structure
```bash
hurdat2_landfall/
│
├── data/
│ └── hurdat2.txt # NOAA dataset (downloaded from NOAA website)
│
├── shapefiles/
│ └── tl_2025_us_state # US state boundary shapefiles
│
├── src/
│ ├── parser.py # Parses HURDAT2 file into structured DataFrame
│ ├── geoutil.py # Geospatial utilities for shapefile & boundary checks
│ ├── detector.py # Landfall detection logic (path & indicator methods)
│ ├── report.py # Exports detected landfalls to CSV
│
├── visualizer.py # Streamlit dashboard application
│
├── requirements.txt # Python dependencies
├── run_app.sh # Linux / macOS setup & run script
├── run_app.bat # Windows setup & run script
└── README.md # Project documentation
```
---

## ⚙️ Setup & Installation

---

### 1. Clone or Download the Project

```bash
git clone https://github.com/ashishhulkoti/Hurricane-Landfall-Detection.git
cd Hurricane-Landfall-Detection
```


### 2. Run script to launch dashboard
#### ▶️ **Linux / macOS**

```bash
chmod +x run_app.sh
./run_app.sh
```
#### ▶️ **Windows**

Double-click run_app.bat

#### Alternatively, you can run the following commands manually

```bash
# Step 1. Create virtual environment
python3 -m venv .venv

# Step 2. Activate the virtual environment
source .venv/bin/activate

# Step 3. Upgrade pip
pip install --upgrade pip

# Step 4. Install dependencies
pip install -r requirements.txt

# Step 5. Run the Streamlit application
streamlit run visualizer.py
```
