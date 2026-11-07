import pandas as pd, re, statistics as st, collections, sys
R='data/raw/'
dfs={s:pd.read_csv(f'{R}{s}.csv') for s in ['workforce','creatives','scientists']}
for s,d in dfs.items():
    print(s,d.shape,list(d.columns),'dupe ids',d.transcript_id.duplicated().sum(),'null text',d.text.isna().sum())
allt=pd.concat(dfs.values())
L=allt.text.str.len(); print('chars min/med/mean/max',L.min(),int(L.median()),int(L.mean()),L.max(),' ~tokens(mean)',int(L.mean()/4))
lab=collections.Counter()
turns=[]
for t in allt.text:
    ls=re.findall(r'(?m)^([A-Za-z ]{1,20}):',t); lab.update(ls); turns.append(len(ls))
print('speaker labels',lab.most_common(8)); print('turns min/med/max',min(turns),int(st.median(turns)),max(turns))
pii={'email':r'[\w.+-]+@[\w-]+\.[\w.]+','phone':r'\b\d{3}[-.\s]\d{3}[-.\s]\d{4}\b','url':r'https?://\S+','handle':r'@\w{3,}'}
for k,p in pii.items():
    n=allt.text.str.count(p); print('PII',k,'transcripts',int((n>0).sum()),'total',int(n.sum()))
print(allt.text.iloc[0][:1200])
