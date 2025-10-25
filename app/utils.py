
import re
from collections import Counter
import numpy as np

LEX_BAD = {
    "fuck":1.5,"fucking":1.5,"shit":1.0,"bitch":1.3,"slut":1.5,
    "idiot":0.8,"stupid":0.7,"moron":0.7,"dumb":0.6,
    "kill":2.0,"die":1.5,"murder":2.2,"hang":2.0,
    "creep":0.7,"pervert":1.0
}

IDENTITY_GROUPS = {
    "black":"Racist language","blacks":"Racist language",
    "asian":"Racist language","asians":"Racist language",
    "jew":"Antisemitic language","jews":"Antisemitic language",
    "muslim":"Islamophobic language","muslims":"Islamophobic language",
    "gay":"Homophobic language","gays":"Homophobic language",
    "lesbian":"Homophobic language","lesbians":"Homophobic language",
}

BASE_TAGS = {
    "toxic":"Abusive / toxic language",
    "severe_toxic":"Severe abuse",
    "obscene":"Obscene language",
    "threat":"Violence / threats",
    "insult":"Harassment / insult",
    "identity_hate":"Hate speech / identity-based"
}

def normalize(t:str)->str:
    t=t.lower()
    t=re.sub(r"https?://\S+|www\.\S+"," ",t)
    t=re.sub(r"[^a-z\s]"," ",t)
    t=re.sub(r"\s+"," ",t).strip()
    return t

def detect_identity_subtags(toks):
    return sorted({IDENTITY_GROUPS[w] for w in toks if w in IDENTITY_GROUPS})

def foulness_meter_0_10(text_norm:str,probs:np.ndarray,labels,thresholds):
    base=6.0*float(np.max(probs))
    toks=re.findall(r"\b[a-z]+\b",text_norm)
    weights=[LEX_BAD[w] for w in toks if w in LEX_BAD]
    lex=min(sum(weights),2.5)
    cnt=Counter([w for w in toks if w in LEX_BAD])
    rep_boost=min(0.5*(max(cnt.values())-1),1.0) if cnt else 0
    num_on=sum(float(probs[i])>=thresholds[labels[i]] for i in range(len(labels)))
    density=min(0.4*num_on,1.0)
    return int(round(max(0,min(10,base+lex+rep_boost+density))))
