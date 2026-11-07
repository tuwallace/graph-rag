"""Score the v3.2 labelling sheets. Usage: uv run --with pandas python scripts/score_labels_v3.py [dir]"""
import sys, math, pandas as pd
D = (sys.argv[1] if len(sys.argv) > 1 else "data/labeling_v3").rstrip("/") + "/"
EDGE = ["ok", "wrong_kind", "wrong_status", "wrong_polarity", "unsupported"]
ATT = ["positive", "negative", "mixed", "none"]
def wilson(k, n, z=1.96):
    if n == 0: return (float("nan"),) * 2
    p = k / n; d = 1 + z * z / n; c = p + z * z / (2 * n); m = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)); return (c - m) / d, (c + m) / d
def fmt(k, n):
    lo, hi = wilson(k, n); return f"{k}/{n} = {k/n:.2f} (95% CI {lo:.2f}-{hi:.2f})" if n else "n/a"
def load(name, key):
    a = pd.read_csv(D + name, dtype={"label": str}); b = pd.read_csv(D + key)
    a["label"] = a["label"].fillna("").str.strip().str.lower(); return a.merge(b, on=["id", "interview"])
e = load("edges_to_label.csv", "edges_key.csv"); done = e[e.label.isin(EDGE)]
print(f"EDGES labelled {len(done)}/{len(e)}   unrecognised labels: {sorted(set(e.label) - set(EDGE) - {''}) or 'none'}")
if len(done):
    n = len(done); ok = (done.label == "ok").sum()
    print("  precision (ok / labelled):", fmt(ok, n), "  <- Gate 1 target 0.80")
    print("  error types:", {k: int((done.label == k).sum()) for k in EDGE[1:]})
    for col, title in [("kind", "by kind"), ("status", "by status the model claimed"), ("group", "by group")]:
        print(f"  {title}:"); [print("    ", k, fmt((g.label == "ok").sum(), len(g))) for k, g in done.groupby(col)]
    print("  by automatic grounding (does it predict correctness?):")
    for k, g in done.groupby("grounded_auto"): print("    grounded" if k else "    ungrounded", fmt((g.label == "ok").sum(), len(g)))
    cur = done[done.status == "current"]; print("  precision on status=current items only:", fmt((cur.label == "ok").sum(), len(cur)))
a = load("attitude_to_label.csv", "attitude_key.csv"); da = a[a.label.isin(ATT)]
print(f"\nATTITUDE labelled {len(da)}/{len(a)}   unrecognised: {sorted(set(a.label) - set(ATT) - {''}) or 'none'}")
if len(da):
    n = len(da); ag = (da.label == da.nimble_attitude).sum(); print("  nimble agreement:", fmt(ag, n))
    print("  confusion (rows = you, cols = nimble):"); print(pd.crosstab(da.label, da.nimble_attitude).to_string())
    po = ag / n; pe = sum((da.label == l).mean() * (da.nimble_attitude == l).mean() for l in ATT); print("  Cohen kappa: %.2f" % ((po - pe) / (1 - pe) if pe < 1 else float("nan")))
    hi, lo = da[da.nimble_conf >= 0.6], da[da.nimble_conf < 0.6]
    print("  agreement at confidence >= 0.6:", fmt((hi.label == hi.nimble_attitude).sum(), len(hi))); print("  agreement at confidence  < 0.6:", fmt((lo.label == lo.nimble_attitude).sum(), len(lo)))
