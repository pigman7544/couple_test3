"""Distinctive editorial previews with transparent symbolic feature traceability.
These are narrative analogies, not predictions or source-verified quotations.
"""
from evidence import ledger
from matcher import rank, transformed, KEYS

LEDGER={e['id']:e for e in ledger()}
AXIS_KO={'attraction':'관계적 결속','security':'안정성','conflict':'긴장','autonomy':'독립성','expression':'표현','growth':'변화·성장'}
# Each profile has a unique editorial contrast, not a fabricated biographical inference.
DETAIL={
'c01':('선택과 약속','외부의 압력에도 약속을 선택하는 장면에 초점을 맞춥니다.','c13','긴 기다림보다 압력 앞에서 내리는 선택이 핵심입니다.'),
'c02':('거리와 재회','정해진 때에 다시 만나는 이야기의 리듬에 초점을 맞춥니다.','c13','오랜 귀환 전략이 아니라 반복되는 분리와 만남이 핵심입니다.'),
'c03':('가능성을 키우는 동행','상대의 잠재력을 알아보고 함께 변화를 만드는 이야기에 초점을 맞춥니다.','f03','재능을 인정하고 추천하는 후원보다 함께 살아가는 과정의 변화가 중심입니다.'),
'c06':('다름을 받아들이는 경계','서로 다른 존재 조건이 신뢰를 시험하는 이야기에 초점을 맞춥니다.','c10','집안의 적대보다 정체성과 경계의 문제가 중심입니다.'),
'c10':('빠른 결속과 충돌','짧은 시간에 강해진 결속과 주변의 적대가 맞물리는 이야기에 초점을 맞춥니다.','c01','오랜 약속의 지속보다 선택의 속도와 외부 충돌이 중심입니다.'),
'c11':('판단을 고치는 관계','첫인상과 편견을 다시 살피며 존중을 쌓는 이야기에 초점을 맞춥니다.','f02','서로 다른 시각의 공존보다 판단의 수정이 핵심입니다.'),
'c13':('능동적인 기다림','부재 속에서도 각자의 판단과 전략을 유지하는 이야기에 초점을 맞춥니다.','c02','주기적 재회보다 오랜 부재에 대처하는 능동성이 중심입니다.'),
'c18':('기대와 현실의 간격','상대의 실제 모습과 마음속 이상 사이의 간격을 살피는 이야기입니다.','c10','상호 결속보다 한쪽의 이상화가 문제의 중심입니다.'),
'f01':('역할이 다른 협력','서로 다른 능력을 결합해 사건을 해결하는 동행에 초점을 맞춥니다.','f03','재능을 알아보는 후원보다 함께 문제를 푸는 협력이 핵심입니다.'),
'f02':('이상과 현실의 동행','서로 다른 현실 인식이 부딪치면서도 동행이 이어지는 이야기에 초점을 맞춥니다.','c11','오해를 바로잡는 사건보다 관점 차이의 지속적인 협상이 중심입니다.'),
'f03':('능력을 알아보는 신뢰','상대의 능력을 알아보고 길을 열어주는 우정에 초점을 맞춥니다.','f01','함께 일하는 기술적 협력보다 인정과 추천이 핵심입니다.'),
'f04':('경쟁에서 유대로','맞서는 힘이 우정으로 바뀌고 상실을 통해 변화하는 이야기에 초점을 맞춥니다.','f02','관점 차이보다 충돌 이후의 깊은 유대가 중심입니다.'),
}

def describe(vector, couple_id, competing_id=None):
    if couple_id not in DETAIL: raise KeyError(couple_id)
    scores=transformed(vector)
    story={c['id']:c for _,_,c in rank(vector)}
    profile=story[couple_id]['story_vector']
    contributions=sorted(((k,((scores[k]-profile[k])/25)**2) for k in KEYS),key=lambda x:(x[1],x[0]))
    # closest axes are 'alignment', not causal evidence or facts about users.
    close=contributions[:2]
    far=contributions[-1]
    theme,anchor,default_rival,contrast=DETAIL[couple_id]
    rival=competing_id or default_rival
    if rival not in DETAIL or rival==couple_id: raise ValueError('invalid comparison')
    other=story[rival]['story_vector']
    # Rank axis differences by how much they contribute to relative distance.
    diffs=sorted(((k, ((scores[k]-other[k])/25)**2-((scores[k]-profile[k])/25)**2) for k in KEYS),key=lambda x:-x[1])
    support=[(k,round(d,3)) for k,d in diffs if d>0]
    caveat='사주에서 만든 상징 점수와 편집자가 설정한 이야기 좌표의 비교일 뿐, 실제 성격·사건·미래를 판정하지 않습니다.'
    return {
      'couple_id':couple_id,'theme':theme,'story_intro_draft':anchor,
      'source_status':LEDGER[couple_id]['source_verification'],
      'symbolic_alignment':[{ 'axis':AXIS_KO[k],'input_score':round(scores[k],2),'story_score':profile[k],'distance_component':round(d,3)} for k,d in close],
      'weak_alignment':{'axis':AXIS_KO[far[0]],'distance_component':round(far[1],3)},
      'comparison':{'other_id':rival,'advantage_axes':[AXIS_KO[k] for k,_ in support[:2]],'relative_distance':round(sum(d for _,d in diffs),3), 'editorial_contrast':contrast if rival==default_rival else '두 서사의 구별점은 각 작품의 관계 구조에서 따로 확인해야 합니다.'},
      'copy':f"'{theme}'이라는 문학적 주제를 제안합니다. {anchor} 계산된 상징 지표 중 {AXIS_KO[close[0][0]]}과 {AXIS_KO[close[1][0]]}이 이 이야기의 편집 좌표에 비교적 가깝습니다. 다만 {AXIS_KO[far[0]]}에서는 차이가 있어, 두 분의 실제 경험과 같다고 단정할 수 없습니다.",
      'disclaimer':caveat
    }
