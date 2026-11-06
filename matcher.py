"""Experimental, deterministic narrative matcher. Not a psychological diagnostic."""
import json, math
from pathlib import Path
DB=json.loads((Path(__file__).parent/'couples.json').read_text(encoding='utf8'))
KEYS=('attraction','security','conflict','autonomy','expression','growth')
# Calibrated reference means/stds: frozen synthetic distribution, not user outcomes.
REFERENCE={'attraction':(56,8),'security':(63,9),'conflict':(57,9),'autonomy':(58,8),'expression':(60,7),'growth':(59,9)}
# Explicitly authored story coordinates, provisional; no automatic quota or forced distribution.
# 0..100, replace 'attraction' with inclusive relational bond.
STORY={
'c01':(72,85,45,65,55,70), # Chunhyang
'c02':(82,60,65,55,40,40), # Weaver
'c03':(60,85,30,40,70,95), # Ondal
'c06':(75,40,85,70,55,50), # White Snake
'c10':(98,25,90,35,90,40), # Romeo
'c11':(60,65,65,85,60,95), # Liz Darcy
'c13':(60,95,40,65,35,60), # Odyssey
'c18':(85,25,75,80,30,30), # Gatsby
'f01':(65,90,25,85,70,80), # Holmes
'f02':(65,60,60,90,85,85), # Quixote
'f03':(55,98,20,65,50,75), # Guan Bao
'f04':(90,75,75,55,90,90), # Gilgamesh
}
for c in DB:
    c['story_vector']=dict(zip(KEYS,STORY[c['id']]))

def transformed(vector):
    # Distribution-aware normalization makes previously compressed input axes comparable.
    # Does not assert meaningful real-world percentile or compatibility.
    return {k:max(0,min(100,50+18*(vector[k]-REFERENCE[k][0])/REFERENCE[k][1])) for k in KEYS}

def rank(vector):
    v=transformed(vector)
    out=[]
    for c in DB:
        # Unitless standardized Euclidean distance, all axes same scale.
        dist=sum(((v[k]-c['story_vector'][k])/25)**2 for k in KEYS)
        out.append((dist,c['id'],c))
    return sorted(out,key=lambda x:(x[0],x[1]))

def winner(vector):return rank(vector)[0][2]
def match(vector,top_k=5):return [x[2] for x in rank(vector)[:top_k]]
