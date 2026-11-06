"""Exploratory, symmetric narrative feature extraction. NOT a validated compatibility model."""
from engine import relationship as legacy
from matcher import KEYS
STEMS='甲乙丙丁戊己庚辛壬癸'; BRANCHES='子丑寅卯辰巳午未申酉戌亥'
ELEMENTS=('wood','fire','earth','metal','water')
STEM_ELEM=('wood','wood','fire','fire','earth','earth','metal','metal','water','water')
BRANCH_ELEM=('water','earth','wood','wood','earth','fire','fire','earth','metal','metal','earth','water')
GEN={'wood':'fire','fire':'earth','earth':'metal','metal':'water','water':'wood'}
CTRL={'wood':'earth','earth':'water','water':'fire','fire':'metal','metal':'wood'}
COMB={frozenset(s) for s in ('子丑','寅亥','卯戌','辰酉','巳申','午未')}
CLASH={frozenset(s) for s in ('子午','丑未','寅申','卯酉','辰戌','巳亥')}
AXES={'attraction':0,'security':0,'conflict':0,'autonomy':0,'expression':0,'growth':0}
def relation(a,b):
    # all cross comparisons are unordered and thus swap invariant
    out={k:50.0 for k in KEYS}; evidence=[]
    def add(delta,label):
        for k,v in delta.items():out[k]+=v
        evidence.append(label)
    # Day stems: element direction and yin-yang distinguish same-element cases
    da,db=STEMS.index(a['day_pillar'][0]),STEMS.index(b['day_pillar'][0])
    ea,eb=STEM_ELEM[da],STEM_ELEM[db]
    if ea==eb: add({'security':9,'expression':5,'conflict':-4},'일간 오행 동일')
    elif GEN[ea]==eb or GEN[eb]==ea: add({'growth':10,'security':5,'attraction':4},'일간 오행 상생')
    else: add({'conflict':10,'growth':4,'attraction':5},'일간 오행 상극')
    if da%2==db%2: add({'expression':5,'security':2},'일간 음양 동일')
    else: add({'attraction':5,'autonomy':4},'일간 음양 상이')
    # Day/month/year branches are progressively lower weighted. Do not infer actual events.
    for label,weight in [('day_pillar',1.0),('month_pillar',0.65),('year_pillar',0.35)]:
        x,y=a[label][1],b[label][1]; pair=frozenset((x,y))
        if pair in COMB: add({'attraction':11*weight,'security':9*weight},f'{label}: 지지 육합')
        elif pair in CLASH: add({'conflict':14*weight,'autonomy':8*weight},f'{label}: 지지 육충')
        else:
            ex,ey=BRANCH_ELEM[BRANCHES.index(x)],BRANCH_ELEM[BRANCHES.index(y)]
            if ex==ey: add({'security':5*weight,'expression':3*weight},f'{label}: 지지 오행 동일')
            elif GEN[ex]==ey or GEN[ey]==ex: add({'growth':7*weight,'security':3*weight},f'{label}: 지지 오행 상생')
            else: add({'conflict':6*weight,'autonomy':4*weight},f'{label}: 지지 오행 상극')
    # Individual five-element composition differences: narrative diversity, not scientific measure
    def profile(p):
        stems=[p[k][0] for k in ('year_pillar','month_pillar','day_pillar')]
        branches=[p[k][1] for k in ('year_pillar','month_pillar','day_pillar')]
        if p.get('hour_pillar'):
            stems.append(p['hour_pillar'][0]);branches.append(p['hour_pillar'][1])
        counts={k:0 for k in ELEMENTS}
        for s in stems: counts[STEM_ELEM[STEMS.index(s)]]+=1
        for s in branches: counts[BRANCH_ELEM[BRANCHES.index(s)]]+=1
        total=sum(counts.values());return {k:v/total for k,v in counts.items()}
    pa,pb=profile(a),profile(b)
    distance=sum(abs(pa[k]-pb[k]) for k in ELEMENTS)/2 # 0..1
    complement=sum(min(pa[k],pb[k]) for k in ELEMENTS)
    add({'autonomy':18*distance,'growth':12*distance,'security':7*complement,'expression':6*complement},'오행 구성 차이/공통성 (편집 가설)')
    return {'vector':{k:round(min(100,max(0,v)),2) for k,v in out.items()},'evidence':evidence,'validation':'전통 상징 기반 미검증 편집 규칙; 실제 관계의 진단·예측 아님','astrology_status':'점성술 점수 미반영'}
