"""Small, explicitly editorial Western tropical Sun-sign component.
Uses the Swiss Ephemeris solar longitude already computed by engine.person.
Not a natal chart, psychological measure, or empirically validated compatibility model.
"""
SIGNS_KO=('양자리','황소자리','쌍둥이자리','게자리','사자자리','처녀자리','천칭자리','전갈자리','사수자리','염소자리','물병자리','물고기자리')
ELEMENTS=('fire','earth','air','water')
SIGN_EN=('Aries','Taurus','Gemini','Cancer','Leo','Virgo','Libra','Scorpio','Sagittarius','Capricorn','Aquarius','Pisces')
DESCS={'fire':'표현과 추진력','earth':'생활의 안정과 꾸준함','air':'대화와 호기심','water':'감정의 교감과 공감'}

def sun_profile(person):
    idx=SIGN_EN.index(person['sun_sign'])
    return {'sign':SIGNS_KO[idx], 'element':ELEMENTS[idx%4], 'theme':DESCS[ELEMENTS[idx%4]]}

def apply_sun_signs(vector,a,b):
    """Bounded symmetric story-selection modifier, at most 3 points/axis."""
    x,y=sun_profile(a)['element'],sun_profile(b)['element']
    v=dict(vector)
    if x==y:
        changes={'expression':2,'security':2}
        description='같은 원소의 태양궁: 비슷한 리듬이라는 이야기'
    elif frozenset((x,y)) in (frozenset(('fire','air')),frozenset(('earth','water'))):
        changes={'growth':3,'attraction':2}
        description='보완하는 원소의 태양궁: 서로를 북돋는 이야기'
    else:
        changes={'autonomy':2,'conflict':2}
        description='서로 다른 리듬의 태양궁: 차이를 조율하는 이야기'
    for key,delta in changes.items():v[key]=round(min(100,max(0,v[key]+delta)),1)
    return v,description

def narrative(a,b):
    x,y=sun_profile(a),sun_profile(b)
    if x['element']==y['element']:
        line='같은 원소라 마음을 움직이는 리듬이 닮았다는 이야기로 읽을 수 있어.'
    elif frozenset((x['element'],y['element'])) in (frozenset(('fire','air')),frozenset(('earth','water'))):
        line='서로의 장점을 살려 주는 조합이라는 이미지로 읽을 수 있어.'
    else:
        line='서로 다른 속도와 표현 방식을 배우는 조합이라는 이미지로 읽을 수 있어.'
    return f'''서양 점성술의 태양궁도 살짝 곁들여 보자. 첫 번째 사람의 태양은 **{x['sign']}**, 두 번째 사람의 태양은 **{y['sign']}**에 있어. 전자는 {x['theme']}, 후자는 {y['theme']}라는 상징과 연결돼. {line}\n\n여기서 사용하는 것은 태어난 날짜의 태양 위치를 바탕으로 한 **태양궁**이야. 상승궁이나 달·행성 간 각도까지 분석하는 전체 출생 차트는 아니야. 사주가 중심이고, 별자리는 관계의 분위기를 덧칠하는 작은 단서로 활용했어.'''
