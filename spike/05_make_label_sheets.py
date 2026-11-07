"""Build blind labelling sheets under data/labeling/ (git-ignored: they contain transcript text)."""
import pandas as pd, json, re, random, csv
R='data/raw/'; OUT='data/labeling/'
tx={};grp={}
for s in ['workforce','creatives','scientists']:
    d=pd.read_csv(f'{R}{s}.csv')
    for t,x in zip(d.transcript_id,d.text): tx[t]=x; grp[t]=s
def pairs(text):
    parts=re.split(r'(?m)^(Assistant|AI|User):\s*',text); turns=list(zip(parts[1::2],parts[2::2])); out=[]; last=None
    for who,body in turns:
        body=body.strip()
        if who in('AI','Assistant'): last=body
        elif last is not None: out.append((last,body))
    return out
def norm(s): return re.sub(r'\s+',' ',re.sub(r"[\"“”'’]",'',s.lower())).strip()
def best_pair(tid,quote):
    q=norm(quote); qt=set(q.split()); best=None;bs=-1
    for qn,an in pairs(tx[tid]):
        if q in norm(an): return qn,an
        sc=len(qt&set(norm(an).split()))/max(1,len(qt))
        if sc>bs: bs,best=sc,(qn,an)
    return best
# ---- 1. edges (from the v2 extraction) ----
E=[json.loads(l) for l in open('data/spike_extract_v2.jsonl')]
items=[(e['transcript_id'],k,it['name'],it['quote'],bool(it['grounded'])) for e in E for k in ['tasks','ai_uses','concerns'] for it in e['extraction'].get(k,[])]
random.seed(2026); samp=random.sample(items,100); random.shuffle(samp)
with open(OUT+'edges_to_label.csv','w',newline='') as f, open(OUT+'edges_key.csv','w',newline='') as g:
    w=csv.writer(f); k=csv.writer(g)
    w.writerow(['id','interview','kind','extracted_name','quote','interviewer_question','participant_answer','label','note'])
    k.writerow(['id','interview','group','kind','grounded_auto'])
    for i,(tid,kind,name,quote,gr) in enumerate(samp,1):
        qn,an=best_pair(tid,quote)
        w.writerow([i,tid,{'tasks':'task','ai_uses':'ai_use','concerns':'concern'}[kind],name,quote,qn[:400],an[:900],'',''])
        k.writerow([i,tid,grp[tid],kind,gr])
# ---- 2. attitude segments (random 30 from the nimble run; model answer hidden) ----
N=pd.read_json('data/spike_nimble.jsonl',lines=True)
random.seed(99); idx=random.sample(range(len(N)),30)
with open(OUT+'attitude_to_label.csv','w',newline='') as f, open(OUT+'attitude_key.csv','w',newline='') as g:
    w=csv.writer(f); k=csv.writer(g)
    w.writerow(['id','interview','interviewer_question','participant_answer','label','note'])
    k.writerow(['id','interview','group','nimble_attitude','nimble_conf'])
    for i,j in enumerate(idx,1):
        r=N.iloc[j]; q,a=r.state.split('\nParticipant: ',1); q=q.replace('Interviewer: ','',1)
        w.writerow([i,r.tid,q[:400],a[:1200],'',''])
        k.writerow([i,r.tid,grp[r.tid],r.attitude,round(float(r.att_conf),3)])
print('wrote',len(samp),'edges and 30 segments to',OUT)
