
from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import joblib,re,numpy as np
from app.utils import normalize,foulness_meter_0_10,BASE_TAGS,detect_identity_subtags,IDENTITY_GROUPS

BIN_ART=joblib.load("models/best_model_logreg_pipeline.pkl")
BIN_PIPE=BIN_ART["pipeline"]
BIN_THR=float(BIN_ART["threshold"])

ML_ART=joblib.load("models/multi_model_pipeline.pkl")
ML_PIPE=ML_ART["pipeline"]
LABELS=list(ML_ART["labels"])
THR={k:float(v) for k,v in ML_ART["thresholds"].items()}

app=FastAPI(title="Tweet Moderation API",version="2.0")
app.mount("/static",StaticFiles(directory="app/static"),name="static")

class Input(BaseModel):
    text:str

@app.get("/")
def root(): return FileResponse("app/static/index.html")

@app.get("/health")
def health(): return {"status":"ok"}

@app.post("/predict")
def predict(i:Input):
    norm=normalize(i.text)
    p_bin=float(BIN_PIPE.predict_proba([norm])[0,1])
    bin_label=int(p_bin>=BIN_THR)
    P=ML_PIPE.predict_proba([norm])[0]
    subs={lab:{"prob":float(P[k]),"label":int(P[k]>=THR[lab])} for k,lab in enumerate(LABELS)}
    tags=[BASE_TAGS[l] for l in LABELS if subs[l]["label"]]
    toks=re.findall(r"\b[a-z]+\b",norm)
    if subs.get("identity_hate",{}).get("label",0)==1 or any(t in IDENTITY_GROUPS for t in toks):
        tags+=detect_identity_subtags(toks)
        if "Hate speech / identity-based" not in tags: tags.append("Hate speech / identity-based")
    meter=foulness_meter_0_10(norm,np.array(P),LABELS,THR)
    return {"binary":{"prob":p_bin,"threshold":BIN_THR,"label":bin_label},"subtypes":subs,"tags":tags,"foulness_meter":meter}
