"""Optional MBTI self-description. Editorial heuristics, not validated compatibility predictions."""
TYPES={a+b+c+d for a in 'EI' for b in 'SN' for c in 'TF' for d in 'JP'}

def normalize(value):
    if value is None or str(value).strip().upper() in {'', 'UNKNOWN', '모름', 'NONE'}:
        return None
    value=str(value).strip().upper()
    if value not in TYPES: raise ValueError('MBTI must be one of 16 types or omitted')
    return value

def mbti_adjustment(a,b):
    """Conservative, symmetrical 6-axis *storytelling* adjustments (max 6 points)."""
    a,b=normalize(a),normalize(b)
    zero={k:0 for k in ('attraction','security','conflict','autonomy','expression','growth')}
    if not a or not b:
        return {'delta':zero,'status':'skipped','evidence':['MBTI 한쪽 이상 미입력: 추가 보정 없음']}
    delta=zero.copy(); evidence=[]
    # Use differences as narrative contrasts, not 'compatibility' claims.
    if a[0]==b[0]:
        delta['expression']+=3; evidence.append('E/I 동일: 교류 선호의 유사성이라는 이야기 단서')
    else:
        delta['autonomy']+=3; evidence.append('E/I 상이: 교류·혼자만의 시간에 관한 차이 단서')
    if a[1]==b[1]:
        delta['security']+=3; evidence.append('S/N 동일: 정보에 주목하는 방식의 유사성 단서')
    else:
        delta['growth']+=3; evidence.append('S/N 상이: 관점 차이에 따른 성장 이야기 단서')
    if a[2]==b[2]:
        delta['expression']+=2; evidence.append('T/F 동일: 판단 선호의 유사성 단서')
    else:
        delta['conflict']+=3; evidence.append('T/F 상이: 의사결정 표현의 차이 단서')
    if a[3]==b[3]:
        delta['security']+=2; evidence.append('J/P 동일: 생활 계획 선호의 유사성 단서')
    else:
        delta['autonomy']+=3; evidence.append('J/P 상이: 계획·유연성의 차이 단서')
    return {'delta':delta,'status':'applied','evidence':evidence}

def enrich(base, mbti_a=None, mbti_b=None):
    m=mbti_adjustment(mbti_a,mbti_b)
    v={k:round(max(0,min(100,x+m['delta'][k])),1) for k,x in base['vector'].items()}
    return {**base,'vector':v,'mbti':{'person_a':normalize(mbti_a),'person_b':normalize(mbti_b),'status':m['status'],'delta':m['delta']},'evidence':base['evidence']+m['evidence']}
