"""Editorial claim ledger. Plot anchors require primary-source verification before publication."""
import json
from pathlib import Path

ARCHETYPES=json.loads((Path(__file__).parent/'archetypes.json').read_text(encoding='utf8'))
# Story-event paraphrases, NOT primary-source citations. Must verify editions/chapters.
ANCHORS={
'c01':('춘향이 변학도의 요구를 거부하고 몽룡과의 약속을 지킨다','압력에 대한 저항','external_pressure'),
'c02':('견우와 직녀가 은하수를 사이에 두고 정해진 때에 만난다','주기적 분리','forced_separation'),
'c03':('평강이 온달과 함께하며 그의 성장을 돕는다','성장 지원','actual_growth'),
'c06':('백소정의 정체가 드러나며 관계가 위기에 놓인다','정체성 경계','identity_secret'),
'c10':('두 연인이 대립하는 가문 사이에서 빠르게 관계를 맺는다','외부 적대와 빠른 결속','family_opposition'),
'c11':('엘리자베스와 다아시가 첫인상과 판단을 수정한다','상호 재평가','actual_change_of_mind'),
'c13':('페넬로페가 구혼자들을 지연시키고 귀환을 기다린다','능동적 기다림','long_absence'),
'c18':('개츠비가 데이지와의 과거를 되살리려 한다','이상화와 투사','idealization'),
'f01':('홈즈의 추리와 왓슨의 기록 및 동행이 함께 작동한다','공동 사건 해결','real_world_cooperation'),
'f02':('돈키호테와 산초가 서로 다른 현실 인식을 지닌 채 여행한다','이상과 현실의 대조','actual_worldview'),
'f03':('포숙아가 관중의 재능을 인정하고 추천한다','재능 인정과 후원','actual_mentorship'),
'f04':('길가메시와 엔키두가 대립 이후 동반자가 된다','경쟁에서 우정으로','actual_conflict_history'),
}
# Distinguish symbolic readings from assertions about actual people and events.
SYMBOLIC={
'day_relation':'일간 오행의 상생·상극·동일 관계',
'yin_contrast':'일간 음양의 같고 다름',
'branch_combination':'연·월·일지의 합 횟수',
'branch_clash':'연·월·일지의 충 횟수',
'element_overlap':'오행 구성의 겹침 정도',
}
PROHIBITED={
'external_pressure','forced_separation','actual_growth','identity_secret','family_opposition',
'actual_change_of_mind','long_absence','idealization','real_world_cooperation',
'actual_worldview','actual_mentorship','actual_conflict_history',
}

def ledger():
    out=[]
    for a in ARCHETYPES:
        plot,interpretation,unobservable=ANCHORS[a['id']]
        out.append({'id':a['id'],'signature':a['signature'],
                    'plot_anchor_draft':plot,'relationship_interpretation':interpretation,
                    'source_verification':'pending_primary_text_check',
                    'actual_life_claim':unobservable,'inferable_from_birth_data':False,
                    'permitted_usage':'literary_analogy_only'})
    return out

def guard_claim(claim,source='birth_data'):
    """Reject real-life assertions from birth data; story analogies allowed if clearly marked."""
    if source=='birth_data' and claim in PROHIBITED:
        raise ValueError('Cannot infer real-world relationship event from birth data: '+claim)
    return True

def preview(couple_id, symbolic_evidence=None):
    entry=next(x for x in ledger() if x['id']==couple_id)
    symbolic_evidence=symbolic_evidence or []
    return {'matched_type':entry['signature'],
            'story_intro_draft':entry['plot_anchor_draft'],
            'story_source_status':'원전 판본·장면 검증 전: 공개 원고로 사용 금지',
            'symbolic_basis':list(symbolic_evidence),
            'interpretation':f"이 관계를 '{entry['signature']}'라는 문학적 비유로 읽습니다.",
            'disclaimer':'출생정보로 실제 성격, 관계 사건, 궁합을 진단하거나 예측하지 않습니다.',
            'not_inferred':entry['actual_life_claim']}

if __name__=='__main__':
    (Path(__file__).parent/'evidence_ledger.json').write_text(json.dumps(ledger(),ensure_ascii=False,indent=2),encoding='utf8')
