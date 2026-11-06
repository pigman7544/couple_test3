"""Small demo web server. Uses existing Python engine; serves real local image assets."""
import json, os, mimetypes
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse
from engine import person
from relationship_v08 import relation
from mbti import enrich
from matcher import rank
from narrative import describe
from story_report import make_report
from astrology import apply_sun_signs, narrative as astrology_narrative

ROOT=Path(__file__).resolve().parent
MAX_BODY=8192

def compute(payload, unlock=False):
    def build(x):
        date=x['date'].split('-')
        if len(date)!=3:raise ValueError('생년월일을 입력해 주세요.')
        t=x.get('time') or None
        hh,mm=map(int,t.split(':')) if t else (None,0)
        return person(*map(int,date),hour=hh,minute=mm,calendar=x.get('calendar','solar'),leap=bool(x.get('leap',False)))
    a,b=build(payload['a']),build(payload['b'])
    rel=enrich(relation(a,b),payload['a'].get('mbti'),payload['b'].get('mbti'))
    rel['vector'], astro_evidence=apply_sun_signs(rel['vector'],a,b)
    rel['astrology_note']=astro_evidence
    ranked=rank(rel['vector']);couple=ranked[0][2]
    story=describe(rel['vector'],couple['id'],ranked[1][2]['id'])
    full=make_report(a,b,rel,couple,story)
    full['astrology']=astrology_narrative(a,b)
    am=payload['a'].get('mbti') or ''
    bm=payload['b'].get('mbti') or ''
    if am and bm: full['mbti_note']=f'선택 입력한 MBTI는 {am}와 {bm}야. 두 유형의 선호 차이를 이야기의 작은 보조 단서로 반영했어. MBTI가 궁합의 좋고 나쁨을 결정하지는 않아.'
    elif am or bm: full['mbti_note']='MBTI는 두 사람 모두 입력했을 때만 매칭의 보조 단서로 활용해. 이번에는 사주와 태양궁을 중심으로 읽었어.'
    else: full['mbti_note']='MBTI는 선택 입력이야. 입력하지 않아도 사주와 태양궁으로 이야기를 만들 수 있어.'
    if unlock:
        return {'full_report':full,'couple':{'id':couple['id'],'name':couple['name'],'work':couple['work']},'has_art':couple['id']=='c06','test_mode':True}
    return {'preview':{'tagline':full['tagline'],'teaser':full.get('teaser',''),'story_excerpt':full.get('story','')[:360]},'couple':{'id':couple['id'],'name':couple['name'],'work':couple['work']},'theme':full['tagline'],'version':'6.4-story-first','has_art':couple['id']=='c06'}

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        path=urlparse(self.path).path
        if path=='/health':raw=b'OK';mime='text/plain; charset=utf-8'
        elif path in ('/','/index.html'):
            raw=(ROOT/'index.html').read_bytes();mime='text/html; charset=utf-8'
        elif path in ('/assets/baek_heo_plain.png','/assets/baek_heo_title.png'):
            raw=(ROOT/path.lstrip('/')).read_bytes();mime='image/png'
        else:self.send_error(404);return
        self.send_response(200)
        self.send_header('Content-Type',mime)
        self.send_header('Content-Length',str(len(raw)))
        self.send_header('Cache-Control','no-cache, must-revalidate')
        self.end_headers();self.wfile.write(raw)
    def do_POST(self):
        endpoint=urlparse(self.path).path
        if endpoint not in ('/api/match','/api/test-unlock'):self.send_error(404);return
        try:
            size=int(self.headers.get('Content-Length','0'))
            if size<=0 or size>MAX_BODY:raise ValueError('입력 형식이 올바르지 않습니다.')
            result=compute(json.loads(self.rfile.read(size)),unlock=(endpoint=='/api/test-unlock'));status=200
        except (ValueError,TypeError,KeyError,IndexError,OverflowError) as e:
            result={'error':str(e)};status=400
        except Exception:
            self.log_error('Unhandled match error',exc_info=True)
            result={'error':'계산 중 오류가 발생했습니다. 입력값을 확인해 주세요.'};status=500
        raw=json.dumps(result,ensure_ascii=False).encode('utf-8')
        self.send_response(status);self.send_header('Content-Type','application/json; charset=utf-8')
        self.send_header('Content-Length',str(len(raw)));self.send_header('Cache-Control','no-store');self.end_headers();self.wfile.write(raw)

if __name__=='__main__':
    port=int(os.environ.get('PORT','8765'))
    print('Open http://localhost:'+str(port),flush=True)
    ThreadingHTTPServer(('0.0.0.0',port),Handler).serve_forever()
