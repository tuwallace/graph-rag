import json, pandas as pd, collections, re, random
E=[json.loads(l) for l in open('data/spike_extract.jsonl')]
print('valid json',sum(e['valid_json'] for e in E),'/',len(E))
n=sum(e['items'] for e in E); g=sum(e['grounded'] for e in E); print('items',n,'grounded quotes',g,'=%.1f%%'%(100*g/n))
secs=[e['secs'] for e in E]; print('secs mean %.1f median %.1f max %.1f total %.0f'%(sum(secs)/len(secs),sorted(secs)[len(secs)//2],max(secs),sum(secs)))
print('est full 1250 transcripts: %.1f h'%(1250*sum(secs)/len(secs)/3600))
for k in ['tasks','ai_uses','concerns']:
    names=[it['name'].strip().lower() for e in E for it in e['extraction'].get(k,[])]
    c=collections.Counter(names); print(k,'items',len(names),'distinct',len(c),'singletons',sum(v==1 for v in c.values()),'top',c.most_common(4))
print('role_guess non-null',sum(bool(e['extraction'].get('role_guess')) for e in E),'/',len(E))
print('attitude',collections.Counter(e['extraction'].get('overall_attitude_to_ai') for e in E))
ungr=[(e['transcript_id'],k,it['name'],it['quote']) for e in E for k in ['tasks','ai_uses','concerns'] for it in e['extraction'].get(k,[]) if not it['grounded']]
print('\nUNGROUNDED examples:'); [print(' ',u) for u in ungr[:6]]
# nimble vs qwen attitude (per transcript: majority of nimble non-none attitudes)
N=pd.read_json('data/spike_nimble.jsonl',lines=True)
print('\nnimble job_worry p>0.5 segments:',int((N.job_worry>0.5).sum()),'of',len(N))
m={}
for t,d in N[N.attitude!='none'].groupby('tid'): m[t]=d.attitude.value_counts().idxmax()
agree=[(m.get(e['transcript_id']),e['extraction'].get('overall_attitude_to_ai')) for e in E]
print('nimble-majority vs qwen overall attitude:',agree)
print('exact agreement',sum(a==b for a,b in agree),'/',len(agree))
random.seed(3); S=[(e['transcript_id'],k,it['name'],it['quote'],it['grounded']) for e in E for k in ['tasks','ai_uses','concerns'] for it in e['extraction'].get(k,[])]
json.dump(random.sample(S,30),open('data/spike_review_sample.json','w'),indent=1)
