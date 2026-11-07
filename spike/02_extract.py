import pandas as pd, json, time, re, random, sys, ollama
MODEL='qwen3:8b-16k'; R='data/raw/'; OUT='data/spike_extract.jsonl'
random.seed(7)
pick=[]
for s,n in [('workforce',10),('creatives',5),('scientists',5)]:
    d=pd.read_csv(f'{R}{s}.csv'); pick+= [(s,r.transcript_id,r.text) for r in d.sample(n,random_state=7).itertuples()]
ENUM=['positive','mixed','negative','unclear']
item={"type":"object","properties":{"name":{"type":"string"},"quote":{"type":"string"}},"required":["name","quote"]}
schema={"type":"object","properties":{
 "role_guess":{"type":["string","null"]},
 "overall_attitude_to_ai":{"type":"string","enum":ENUM},
 "tasks":{"type":"array","items":item},"ai_uses":{"type":"array","items":item},"concerns":{"type":"array","items":item}},
 "required":["role_guess","overall_attitude_to_ai","tasks","ai_uses","concerns"]}
PROMPT="""You read an interview transcript about how a professional uses AI at work. Extract ONLY what the participant (the "User" turns) said.
- tasks: work tasks the participant does (short lowercase noun phrase, e.g. "writing sales pitches").
- ai_uses: ways the participant uses, or chooses not to use, AI (e.g. "drafting emails").
- concerns: worries or frustrations about AI (e.g. "losing skills").
- role_guess: their job if stated or clearly implied, else null.
- overall_attitude_to_ai: positive, mixed, negative or unclear.
Every item needs a "quote": an exact copied span of at most 25 words from a User turn. Do not invent items. Empty lists are fine.

TRANSCRIPT:
"""
def norm(s): return re.sub(r'\s+',' ',re.sub(r"[\"“”'’]",'',s.lower())).strip()
client=ollama.Client(); out=open(OUT,'w'); tot=0
for i,(split,tid,text) in enumerate(pick):
    t0=time.time()
    r=client.chat(model=MODEL,messages=[{"role":"user","content":PROMPT+text}],format=schema,think=False,options={"temperature":0,"num_ctx":16384})
    dt=time.time()-t0
    try: j=json.loads(r['message']['content']); ok=True
    except Exception as e: j={}; ok=False
    nt=norm(text); g=n=0
    for k in ['tasks','ai_uses','concerns']:
        for it in j.get(k,[]):
            n+=1; it['grounded']= bool(it.get('quote')) and norm(it['quote']) in nt; g+=it['grounded']
    rec={"split":split,"transcript_id":tid,"secs":round(dt,1),"valid_json":ok,"items":n,"grounded":g,"eval_tokens":r.get('eval_count'),"prompt_tokens":r.get('prompt_eval_count'),"extraction":j}
    out.write(json.dumps(rec)+'\n'); out.flush(); tot+=dt
    print(f"{i+1}/20 {tid} {dt:.1f}s items={n} grounded={g} json={ok}",flush=True)
print('total secs',round(tot,1))
