# 🦅 Garuda v1: 10km² Geospatial Sector Reconnaissance CLI

A terminal-based geospatial intelligence tool that accepts geographic coordinates (**Latitude** & **Longitude**), calculates an exact **10 km × 10 km (100 km²)** square bounding box, and aggregates deep spatial metrics using free public APIs.

---

## ⚡ Core Capabilities

- **Precision Geodesic Bounding Box**: Uses WGS84 ellipsoidal math to compute a true 10 km × 10 km square sector (5 km north/south, 5 km east/west) centered on the target coordinate.
- **Housing & Structural Footprint**:
  - Total building count & building density per km².
  - Categorization into residential houses, multi-family apartments, commercial/industrial facilities, and civic structures.
- **Road & Transportation Network**:
  - Complete highway network count & road density per km².
  - Breakdown by infrastructure tier: Expressways/Trunks, Primary/Secondary avenues, Residential/Local streets, Service/Living streets, and Rural tracks.
  - Active mobility (pedestrian walkways & cycleways).
  - Transit & engineering crossings: Bridges, Tunnels, and Railway tracks.
- **Critical & Emergency Infrastructure**:
  - Hospitals, Outpatient Clinics, and Pharmacies.
  - Police Stations, Emergency Response Posts, and Fire Stations.
  - Educational hubs: Primary/Secondary Schools and Higher Education Universities/Colleges.
- **Civic Amenities & Environmental Ecology**:
  - Water bodies (rivers, lakes, canals, reservoirs).
  - Urban green cover, gardens, and parks.
  - Financial access (Banks and ATMs).
  - Mobility energy points (Fuel and EV Charging stations).
  - Places of worship and food markets/supermarkets.
- **Strategic Sector Assessment**:
  - Urbanization density rating (Hyper-Dense Urban, Developed Urban Center, Suburban, Semi-Rural, Rural).
  - Infrastructure Maturity Score (Tier-1 to Tier-4 index out of 100).
- **Zero API Keys Required**: Driven entirely by public OpenStreetMap, Nominatim Reverse Geocoding, and Open-Meteo APIs with automated fallbacks and mirror rotation.

---

## 🚀 Installation & Prerequisites

Python 3.9+ is required.

```bash
# Clone or navigate to the repository
cd "Garuda v1"

# Install dependencies
pip install -r requirements.txt
```

Dependencies:
- `requests` (API communication & network failover)
- `rich` (Terminal tables, panels, spinners, and ANSI formatting)
- `pydantic` (Validated geospatial data models)
- `click` (CLI command argument parsing)

---

## 💻 Usage

### 1. Interactive Terminal Mode
Run without arguments to enter interactive mode with preset coordinates or custom input:

```bash
python garuda_app.py
```

### 2. Direct CLI Arguments
Provide coordinates directly via `--lat` and `--lon`:

```bash
# Bengaluru Center
python garuda_app.py --lat 12.9716 --lon 77.5946

# Manhattan, New York City
python garuda_app.py --lat 40.7580 --lon -73.9855

# London Center
python garuda_app.py --lat 51.5074 --lon -0.1278

# Tokyo Shibuya
python garuda_app.py --lat 35.6580 --lon 139.7016
```

### 3. Custom Sector Size
To analyze an area different from 10 km (e.g. 5 km or 15 km):

```bash
python garuda_app.py --lat 12.9716 --lon 77.5946 --size 15.0
```

### 4. Exporting Reports
Export the generated intelligence directly to JSON or Markdown:

```bash
# Export to Markdown
python garuda_app.py --lat 12.9716 --lon 77.5946 --export md --output bengaluru_report.md

# Export to JSON
python garuda_app.py --lat 40.7580 --lon -73.9855 --export json --output nyc_sector.json
```

---

## 🧪 Testing

Execute the test suite:

```bash
python -m unittest discover tests
```

---

## 📂 Architecture

```
Garuda v1/
├── garuda_app.py          # Root CLI executable script
├── requirements.txt       # Dependencies
├── README.md              # Project documentation
├── garuda/
│   ├── __init__.py        # Package definition
│   ├── __main__.py        # Module entrypoint (python -m garuda)
│   ├── cli.py             # Click CLI & interactive prompt handler
│   ├── geo.py             # Geodesic square bounding box calculations
│   ├── models.py          # Pydantic schemas for sector reports
│   ├── engine.py          # Reconnaissance coordinator & concurrent fetcher
│   ├── analyzer.py        # Density indices & infrastructure scoring
│   ├── ui.py              # Rich terminal layout, tables & panels
│   └── apis/
│       ├── __init__.py
│       ├── nominatim.py   # Reverse geocoding & POI search
│       ├── overpass.py    # OpenStreetMap Overpass client & mirrors
│       └── elevation.py   # Open-Meteo elevation & climate metrics
└── tests/
    ├── test_geo.py        # Coordinate math & bounding box validation
    └── test_pipeline.py   # Analyzer scoring & model verification
```
