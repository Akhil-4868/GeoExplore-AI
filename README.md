# GeoExplore AI 🌍
### AI-Powered Geological Exploration & Geochemical Prospectivity Analysis

GeoExplore AI is a full-stack geological exploration platform designed to analyze geochemical datasets, visualize geological observations and identify potentially interesting exploration zones using machine learning and geospatial visualization.

The platform combines interactive mapping, geochemical data analysis and machine learning to help users explore geological datasets through an intuitive dashboard.

## 🚀 Key Features

- **Interactive Geological Map:** Visualize geological sampling locations using geographic coordinates.
- **Geochemical Data Analysis:** Analyze copper, zinc, iron and magnetic measurements.
- **CSV Dataset Upload:** Upload custom geological datasets for analysis.
- **Machine Learning:** Random Forest classification when sufficient labeled observations are available.
- **Anomaly Scoring:** Generate relative geochemical anomaly rankings when labeled data is insufficient.
- **Data Visualization:** Explore geochemical patterns through interactive charts.
- **Dataset Management:** Inspect geological observations and export analysis results.

## 🛠️ Technology Stack

| Component | Technologies |
|---|---|
| Frontend | React.js, JavaScript, CSS |
| Backend | Python, FastAPI |
| Data Processing | Pandas, NumPy |
| Machine Learning | Scikit-learn, Random Forest |
| Visualization | Leaflet, Recharts |
| API | REST API |

## 🏗️ Project Architecture

```text
GeoExplore-AI/
│
├── backend/
│   ├── main.py
│   └── requirements.txt
│
├── frontend/
│   ├── src/
│   │   ├── main.jsx
│   │   └── style.css
│   ├── index.html
│   ├── package.json
│   └── package-lock.json
│
├── .gitignore
└── README.md
```

## ⚙️ Installation and Setup

### Prerequisites

- Python 3.10+
- Node.js 20+
- npm
- Git

### 1. Clone the repository

```bash
git clone https://github.com/Akhil-4868/GeoExplore-AI.git
cd GeoExplore-AI
```

### 2. Setup the backend

```powershell
cd backend
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

Start the backend:

```powershell
.\.venv\Scripts\python.exe -m uvicorn main:app --reload --port 8000
```

Backend API:
http://localhost:8000

API documentation:
http://localhost:8000/docs

### 3. Setup the frontend

Open a second terminal:

```powershell
cd frontend
npm install
npm run dev
```

Frontend:
http://localhost:5173

## 📊 Dataset Format

The platform accepts CSV datasets containing the following columns:

| Column | Description |
|---|---|
| latitude | Geographic latitude |
| longitude | Geographic longitude |
| copper_ppm | Copper concentration |
| zinc_ppm | Zinc concentration |
| iron_pct | Iron percentage |
| magnetic_nt | Magnetic measurement |
| target | Optional binary target label |

The optional `target` column represents known positive and negative classes.

When sufficient labeled observations are available, the application trains a Random Forest classifier and evaluates it using a holdout dataset.

Otherwise, a relative rank-based anomaly score is calculated.

## 🧠 Machine Learning Approach

The platform uses two analysis approaches:

1. **Supervised Learning:** Random Forest classification using labeled geochemical observations.
2. **Unsupervised-style Ranking:** A relative geochemical anomaly scoring approach when sufficient labeled data is unavailable.

These outputs are exploratory indicators and should not be interpreted as validated mineral deposit probabilities.

## ⚠️ Limitations

- The application is an exploratory MVP, not a validated mineral discovery system.
- Sample observations and labels are synthetic.
- Uploaded datasets are processed in memory.
- Models are not persisted between sessions.
- Spatially correlated observations can cause optimistic evaluation results.
- Geological interpretations require domain expertise and field validation.

## 🔮 Future Improvements

- PostgreSQL and PostGIS integration.
- User authentication and project management.
- Integration of real public geological datasets.
- Advanced spatial machine learning.
- 3D geological modelling.
- Remote sensing and satellite data integration.
- Automated geological report generation.

## 👨‍💻 Author

**Akhil**

Integrated M.Tech – Applied Geology

IIT (ISM) Dhanbad

GitHub: https://github.com/Akhil-4868

---

*GeoExplore AI is developed as an interdisciplinary project combining geology, geospatial analysis, machine learning and full-stack software engineering.*
