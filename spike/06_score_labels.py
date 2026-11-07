"""Score filled-in labelling sheets. Usage: python spike/06_score_labels.py [labeling_dir]"""
import sys, math, collections, pandas as pd
D=(sys.argv[1] if len(sys.argv)>1 else 'data/labeling').rstrip('/')+'/'
def wilson(k,n,z=1.96):
    if n==0: return (float('nan'),)*2
    p=k/n; d=1+z*z/n; c=p+z*z/(2*n); m=z*math.sqrt(p*(1-p)/n+z*z/(4*n*n)); return ((c-m)/d,(c+m)/d)
def fmt(k,n): lo,hi=wilson(k,n); return f'{k}/{n} = {k/n:.2f}  (95% CI {lo:.2f}-{hi:.2f})' if n else 'n/a'
# ---- edges ----
e=pd.read_csv(D+'edges_to_label.csv',dtype={'label':str}).merge(pd.read_csv(D+'edges_key.csv'),on=['id','interview','kind'] if False else ['id','interview'],suffixes=('','_k'))
e['label']=e['label'].fillna('').astype(str).str.strip().str.lower()
done=e[e.label.isin(['ok','hypo','wrong'])]
print(f'EDGES labelled {len(done)}/{len(e)}  (bad labels: {sorted(set(e.label)-set(["ok","hypo","wrong",""]))})')
if len(done):
    n=len(done); ok=(done.label=='ok').sum(); wr=(done.label=='wrong').sum(); hy=(done.label=='hypo').sum()
    print('  strict precision  (only "wrong" is an error):',fmt(n-wr,n))
    print('  lenient precision (hypo + wrong are errors) :',fmt(ok,n),' <- ADR-0010 compares this to the 0.80 target AFTER the verify step; before it, expect lower')
    print('  breakdown: ok',ok,'hypo',hy,'wrong',wr)
    print('  by kind:'); [print('   ',k,fmt((g.label=="ok").sum(),len(g))) for k,g in done.groupby('kind')]
    print('  by group:'); [print('   ',k,fmt((g.label=="ok").sum(),len(g))) for k,g in done.groupby('group')]
    gr=done.groupby('grounded_auto'); print('  by auto-grounding (does the grounding check predict correctness?):')
    for k,g in gr: print('    grounded' if k else '    ungrounded',fmt((g.label=="ok").sum(),len(g)))
# ---- attitude ----
a=pd.read_csv(D+'attitude_to_label.csv',dtype={'label':str}).merge(pd.read_csv(D+'attitude_key.csv'),on=['id','interview'])
a['label']=a['label'].fillna('').astype(str).str.strip().str.lower()
L=['positive','negative','mixed','none']; done=a[a.label.isin(L)]
print(f'\nATTITUDE labelled {len(done)}/{len(a)}  (bad labels: {sorted(set(a.label)-set(L)-{""})})')
if len(done):
    n=len(done); ag=(done.label==done.nimble_attitude).sum(); print('  nimble agreement with you:',fmt(ag,n))
    print('  confusion (rows = your label, cols = nimble):'); print(pd.crosstab(done.label,done.nimble_attitude).to_string())
    po=ag/n; pe=sum((done.label==l).mean()*(done.nimble_attitude==l).mean() for l in L); print('  Cohen kappa: %.2f'%((po-pe)/(1-pe) if pe<1 else float('nan')))
    hi=done[done.nimble_conf>=0.6]; lo=done[done.nimble_conf<0.6]
    print('  agreement when nimble confidence >=0.6:',fmt((hi.label==hi.nimble_attitude).sum(),len(hi)))
    print('  agreement when nimble confidence  <0.6:',fmt((lo.label==lo.nimble_attitude).sum(),len(lo)))
