from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from io import BytesIO

app = FastAPI(title='GeoExplore AI API', version='1.0')
app.add_middleware(CORSMiddleware, allow_origins=['http://localhost:5173'], allow_methods=['*'], allow_headers=['*'])
DATA = None
FEATURES = ['latitude','longitude','copper_ppm','zinc_ppm','iron_pct','magnetic_nt']

class PredictionInput(BaseModel):
    latitude: float
    longitude: float
    copper_ppm: float
    zinc_ppm: float
    iron_pct: float
    magnetic_nt: float

@app.get('/api/health')
def health(): return {'status':'ok'}

@app.get('/api/sample')
def sample():
    rng = np.random.default_rng(42)
    n = 180
    lat = rng.uniform(21,26,n); lon = rng.uniform(80,87,n)
    copper = rng.gamma(2,35,n); zinc = rng.gamma(2,45,n)
    iron = rng.uniform(1,20,n); magnetic = rng.normal(44000,2500,n)
    # Artificial teaching labels; not geological ground truth.
    score = .03*copper + .018*zinc + .25*iron + .0001*(magnetic-44000)
    label = (score > np.quantile(score,.67)).astype(int)
    df = pd.DataFrame({'latitude':lat,'longitude':lon,'copper_ppm':copper,'zinc_ppm':zinc,'iron_pct':iron,'magnetic_nt':magnetic,'target':label})
    return {'rows':df.round(3).to_dict('records'),'synthetic':True}

@app.post('/api/analyze')
async def analyze(file: UploadFile = File(...)):
    if not file.filename.lower().endswith('.csv'): raise HTTPException(400,'Upload a CSV file')
    raw = await file.read()
    if len(raw)>5_000_000: raise HTTPException(413,'CSV exceeds 5 MB')
    try: df = pd.read_csv(BytesIO(raw))
    except Exception: raise HTTPException(400,'Invalid CSV')
    missing = [c for c in FEATURES if c not in df.columns]
    if missing: raise HTTPException(400,'Missing columns: '+', '.join(missing))
    if len(df)>10000: raise HTTPException(400,'Maximum 10,000 rows')
    df = df.copy()
    for c in FEATURES: df[c] = pd.to_numeric(df[c],errors='coerce')
    df = df.replace([np.inf,-np.inf],np.nan).dropna(subset=FEATURES)
    df = df[df.latitude.between(-90,90)&df.longitude.between(-180,180)]
    if df.empty: raise HTTPException(400,'No valid rows')
    model_info = {'mode':'heuristic','validation_accuracy':None}
    if 'target' in df.columns:
        df['target'] = pd.to_numeric(df['target'],errors='coerce')
        train = df[df.target.isin([0,1])]
        if len(train)>=30 and train.target.value_counts().min()>=8:
            Xtr,Xte,ytr,yte = train_test_split(train[FEATURES],train.target.astype(int),test_size=.25,random_state=42,stratify=train.target)
            model = RandomForestClassifier(n_estimators=120,random_state=42,class_weight='balanced')
            model.fit(Xtr,ytr)
            model_info={'mode':'supervised random forest','validation_accuracy':round(float(accuracy_score(yte,model.predict(Xte))),3)}
            df['score'] = model.predict_proba(df[FEATURES])[:,list(model.classes_).index(1)]*100
        else: model_info['warning']='Target column requires at least 30 labeled rows and 8 per class.'
    if 'score' not in df:
        # Relative anomaly ranking only, not a calibrated deposit probability.
        ranked = pd.DataFrame({c:df[c].rank(pct=True) for c in ['copper_ppm','zinc_ppm','iron_pct','magnetic_nt']})
        df['score'] = (ranked.mean(axis=1)*100).round(2)
    df['risk'] = pd.cut(df.score,[-1,40,70,101],labels=['Low','Medium','High'])
    return {'rows':df[FEATURES+['score','risk']].round(3).to_dict('records'),'count':len(df),'model':model_info,'note':'Screening scores are exploratory, not proof of mineral deposits. Validate with fieldwork and independent geological evidence.'}
