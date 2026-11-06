"""Exploratory storytelling engine. Traditional symbolism, NOT psychological prediction."""
from datetime import datetime, timezone, timedelta
from korean_lunar_calendar import KoreanLunarCalendar
import swisseph as swe
from matcher import match, KEYS
STEMS='甲乙丙丁戊己庚辛壬癸'; BRANCHES='子丑寅卯辰巳午未申酉戌亥'
ELEMENT=['wood','wood','fire','fire','earth','earth','metal','metal','water','water']
# Conventional five-element generation and control cycles
GEN={'wood':'fire','fire':'earth','earth':'metal','metal':'water','water':'wood'}
CTRL={'wood':'earth','earth':'water','water':'fire','fire':'metal','metal':'wood'}
S = ['Aries','Taurus','Gemini','Cancer','Leo','Virgo','Libra','Scorpio','Sagittarius','Capricorn','Aquarius','Pisces']

def longitude(dt):
    utc=dt.astimezone(timezone.utc)
    jd=swe.julday(utc.year,utc.month,utc.day,utc.hour+utc.minute/60+utc.second/3600)
    return swe.calc_ut(jd,swe.SUN)[0][0]

def person(year,month,day,hour=None,minute=0,calendar='solar',leap=False):
    c=KoreanLunarCalendar()
    if calendar=='solar': ok=c.setSolarDate(year,month,day)
    elif calendar=='lunar': ok=c.setLunarDate(year,month,day,leap)
    else: raise ValueError('calendar must be solar or lunar')
    if not ok: raise ValueError('Unsupported or invalid date (calendar supports 1000–2050)')
    if hour is not None and (not 0<=hour<=23 or not 0<=minute<=59): raise ValueError('Invalid time')
    y,m,d=c.solarYear,c.solarMonth,c.solarDay
    dt=datetime(y,m,d,hour if hour is not None else 12,minute if hour is not None else 0,tzinfo=timezone(timedelta(hours=9)))
    lon=longitude(dt)
    # Solar-term year begins at 315° (approx. Ipchun); month advances in 30° steps.
    solar_year=y if lon>=315 or lon<45 and m>=2 else y-1
    # More robust across Jan/Feb: 315..360 = current year, 0..315 = current year except Jan/early Feb.
    solar_year=y if (m>2 or (m==2 and lon>=315)) else y-1
    yi=(solar_year-1984)%60
    year_p=STEMS[yi%10]+BRANCHES[yi%12]
    mi=int(((lon-315)%360)//30)  # tiger month index 0
    month_branch=BRANCHES[(2+mi)%12]
    tiger_stem=(2*(yi%10)+2)%10 # 甲年丙寅, 乙年戊寅...
    month_stem=STEMS[(tiger_stem+mi)%10]
    # Day pillar from calendar's Korean gapja, based on civil date, not 23:00 rollover.
    day_p=c.getChineseGapJaString().split(' ')[2].replace('日','')
    di=STEMS.index(day_p[0]); day_branch=BRANCHES.index(day_p[1])
    hour_p=None
    if hour is not None:
        hi=((hour+1)//2)%12
        hour_p=STEMS[((di%5)*2+hi)%10]+BRANCHES[hi]
    sign=S[int(lon//30)]
    return {'solar_date':f'{y:04d}-{m:02d}-{d:02d}', 'year_pillar':year_p,'month_pillar':month_stem+month_branch,'day_pillar':day_p,'hour_pillar':hour_p,'day_element':ELEMENT[di], 'solar_longitude':round(lon,3),'sun_sign':sign,'notes':['23:00 day rollover convention not applied','birthplace assumed Korea (UTC+9)','solar-term boundaries may vary by ephemeris and school']}

def relationship(a,b):
    # Transparent, deliberately modest prototype effects; not validated coefficients.
    scores=dict.fromkeys(KEYS,50.0); evidence=[]
    x,y=a['day_element'],b['day_element']
    if x==y:
        for k,v in {'security':12,'expression':8,'conflict':-5}.items(): scores[k]+=v
        evidence.append('일간 오행 동일: 친숙함이라는 상징적 해석')
    elif GEN[x]==y or GEN[y]==x:
        for k,v in {'security':8,'growth':13,'attraction':5}.items(): scores[k]+=v
        evidence.append('일간 오행 상생 관계: 지원·성장의 상징적 해석')
    elif CTRL[x]==y or CTRL[y]==x:
        for k,v in {'conflict':16,'growth':6,'attraction':5}.items(): scores[k]+=v
        evidence.append('일간 오행 상극 관계: 긴장·변화의 상징적 해석')
    # Conventional six-combinations and six-clashes for day branches.
    combine={frozenset(p) for p in ['子丑','寅亥','卯戌','辰酉','巳申','午未']}
    clash={frozenset(p) for p in ['子午','丑未','寅申','卯酉','辰戌','巳亥']}
    pair=frozenset([a['day_pillar'][1],b['day_pillar'][1]])
    if pair in combine:
        scores['security']+=13; scores['attraction']+=9; evidence.append('일지 육합: 결속의 상징')
    if pair in clash:
        scores['conflict']+=19; scores['autonomy']+=8; evidence.append('일지 육충: 차이·마찰의 상징')
    # Astrology deliberately NOT incorporated into numeric score until rules are specified.
    return {'vector':{k:round(min(100,max(0,v)),1) for k,v in scores.items()},'evidence':evidence,'astrology_status':'태양궁 표시만 지원; 점수 반영하지 않음','validation':'미검증 편집 규칙; 실제 관계 진단·예측 아님'}

def report(a,b,top_k=5):
    rel=relationship(a,b)
    return {'person_a':a,'person_b':b,'relationship':rel,'matches':match(rel['vector'],top_k=top_k)}

if __name__=='__main__':
    import json
    a=person(1992,3,18,16);b=person(1992,4,30,1)
    print(json.dumps(report(a,b,3),ensure_ascii=False,indent=2))
