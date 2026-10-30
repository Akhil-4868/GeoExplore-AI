# GeoExplore AI

A full-stack exploratory geochemical prospectivity dashboard built with React, Leaflet, Recharts, FastAPI, Pandas and scikit-learn.

## Requirements
- Node.js 20+ and npm
- Python 3.10+

## Run backend (Windows PowerShell)
```powershell
cd backend
py -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```
If PowerShell blocks activation, run `.\.venv\Scripts\python.exe -m pip install -r requirements.txt` and `.\.venv\Scripts\python.exe -m uvicorn main:app --reload --port 8000` instead.

## Run frontend (second terminal)
```powershell
cd frontend
npm install
npm run dev
```
Open http://localhost:5173 . API docs: http://localhost:8000/docs .

## Input CSV columns
Required: `latitude,longitude,copper_ppm,zinc_ppm,iron_pct,magnetic_nt`
Optional: `target` (binary 0/1, 1 denotes a known positive class). With >=30 labeled rows and >=8 per class, the API trains a random forest and reports holdout accuracy. Otherwise it computes a relative rank-based anomaly score, **not** mineral probability.

Use **Load sample dataset** to test the full pipeline without files. Sample observations and labels are SYNTHETIC.

## Limitations
- This is a working MVP, not a validated mineral discovery system.
- CSVs are processed in memory; no database or accounts in this version.
- Model trained on uploaded labeled data is not persisted.
- Random train/test split may overestimate performance on spatially correlated geology data; use spatial cross-validation for research use.
- The heuristic ranking assumes higher concentrations correspond to higher interest, which is not universally geologically valid.
- Do not use these results for operational exploration decisions without field validation.

## GitHub
Create an empty repository on GitHub named `geoexplore-ai` (do not pre-add README), then from the project root:
```bash
git init -b main
git add .
git commit -m "Initial GeoExplore AI MVP"
git remote add origin https://github.com/YOUR_USERNAME/geoexplore-ai.git
git push -u origin main
```
Never commit credentials, tokens, private datasets or `.env` files.
