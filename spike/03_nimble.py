import pandas as pd, json, time, re, requests, collections, statistics as st
R='data/raw/'; URL='http://localhost:11434/v1/systemone'
ids=[json.loads(l)['transcript_id'] for l in open('data/spike_extract.jsonl')]
tx={}
for s in ['workforce','creatives','scientists']:
    d=pd.read_csv(f'{R}{s}.csv'); tx.update(dict(zip(d.transcript_id,d.text)))
def pairs(text):
    parts=re.split(r'(?m)^(Assistant|AI|User):\s*',text); turns=list(zip(parts[1::2],parts[2::2]))
    out=[];last=None
    for who,body in turns:
        body=body.strip()
        if who in('AI','Assistant'): last=body
        elif last is not None: out.append((last,body))
    return out
Q={
 "attitude":{"type":"choice","instructions":"What is the participant's attitude toward AI in this answer?","criteria":{"positive":"favourable or satisfied","negative":"unfavourable, frustrated or distrustful","mixed":"both good and bad","none":"no attitude expressed (facts, consent, small talk)"}},
 "topic":{"type":"choice","instructions":"What is this answer mainly about?","criteria":{"task":"the work the participant does","ai_use":"how they use or avoid AI","concern":"worries or frustrations about AI","skills_future":"skills or the future of their work with AI","other":"anything else, including consent and greetings"}},
 "job_worry":{"type":"noul","instructions":"Does the participant express worry about their job or income being affected by AI?"}}
rows=[];lat=[];errs=collections.Counter()
for tid in ids:
    for qn,ans in pairs(tx[tid]):
        state=f"Interviewer: {qn}\nParticipant: {ans}"
        t0=time.time(); r=requests.post(URL,json={"model":"nimble","state":state,"questions":Q},timeout=120); dt=time.time()-t0
        if r.status_code!=200: errs[r.text[:120]]+=1; continue
        a=r.json()['answers']; lat.append(dt)
        rows.append({"tid":tid,"state":state,"secs":dt,"in_tok":r.json()['usage']['input_tokens'],
          "attitude":a['attitude']['choice'],"att_conf":a['attitude']['confidence'],
          "topic":a['topic']['choice'],"topic_conf":a['topic']['confidence'],"job_worry":a['job_worry'].get('noul')})
        if len(rows)==1: print(json.dumps(r.json()['answers'])[:600])
pd.DataFrame(rows).to_json('data/spike_nimble.jsonl',orient='records',lines=True)
print('segments',len(rows),'errors',dict(errs))
if lat: 
    s=sorted(lat); print('latency s: p50 %.2f p95 %.2f max %.2f total %.0f'%(st.median(s),s[int(len(s)*.95)],s[-1],sum(s)))
df=pd.DataFrame(rows)
if len(df):
    print(df.attitude.value_counts().to_dict()); print(df.topic.value_counts().to_dict()); print(df.job_worry.value_counts().to_dict())
    print('conf mean att %.2f topic %.2f; share att_conf<0.6: %.2f'%(df.att_conf.mean(),df.topic_conf.mean(),(df.att_conf<0.6).mean()))
    print('max input tokens',df.in_tok.max())
