"""PII residual checks from ADR-0012: phone formats, first names on their own, employers (any capitalisation).
It finds candidates in the participant turns of data/raw, then reports which of them occur in a TRACKED file (what the public repo exposes).
Only counts and the location of tracked-file hits are printed; the candidates themselves stay on the local machine (printed only with --show).
Run: uv run python scripts/pii_residuals.py [--show] [--history]      Exit 1 if any candidate occurs in a tracked file.
Heuristic, not a guarantee: names that are also common words, and employers described without a pattern, are not found.
"""
import csv, collections, pathlib, re, subprocess, sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
SHOW = "--show" in sys.argv
csv.field_size_limit(10**9)
PHONE = re.compile(r"(?<!\d)(?:\+?\d{1,2}[\s.-]?)?(?:\(\d{3}\)|\d{3})[\s.-]\d{3}[\s.-]\d{4}(?!\d)|(?<!\d)\+\d{8,14}(?!\d)")
NAME_INTRO = re.compile(r"\b(?:my name is|my name's|call me|i am called|this is)\s+([A-Z][a-z]{2,15})\b")
EMPLOYER = re.compile(r"\b(?:work(?:ed|ing|s)?|employed|intern(?:ed|ing)?|contract(?:ed|ing)?|consult(?:ed|ing)?)\s+(?:at|for|with)\s+((?:[A-Z][\w&.'-]*)(?:\s+[A-Z][\w&.'-]*){0,3})")
EMPLOYER2 = re.compile(r"\b(?:my (?:company|employer|firm|organisation|organization|university|school)|our company)\s+(?:is|called|named)\s+((?:[A-Z][\w&.'-]*)(?:\s+[A-Z][\w&.'-]*){0,3})")
ADDRESS = re.compile(r"\b(?:Hi|Hello|Hey|Thanks|Thank you|Dear)[,]?\s+([A-Z][a-z]{2,15})\b[,!.]|\b(?:I'm|I am)\s+([A-Z][a-z]{2,15})\b")
# Reviewed by hand on 2026-11-10: each is a product, vendor, document heading or sentence fragment, not a person or a participant's employer.
ALLOW = {"Claude", "Chat", "A LOT", "AI's", "HTML", "Google", "Linux", "Microsoft", "Postgres", "Sheets", "Descriptions", "Questions", "Rules", "Scores", "Scripts", "Secrets", "Stats", "Wheels", "Reports", "Integrated"}
STOP_EMP = {"the", "a", "an", "home", "myself", "my", "our", "us", "this", "that", "it"}


def participant_text(text):
    out = []
    for line in text.splitlines():
        m = re.match(r"\s*(?:User|Human|Participant)\s*:\s*(.*)", line)
        if m: out.append(m.group(1))
    return "\n".join(out) or text


def tracked():
    out = subprocess.run(["git", "ls-files", "-z"], cwd=ROOT, capture_output=True, check=True).stdout.decode().split("\0")
    return [ROOT / p for p in out if p and (ROOT / p).suffix in {".md", ".py", ".json", ".yml", ".yaml", ".toml", ".txt", ".cfg", ".example", ".sh", ".html", ""} and (ROOT / p).exists() and (ROOT / p).stat().st_size < 3_000_000]


def main():
    words, proper = set(), set()
    dp = pathlib.Path("/usr/share/dict/words")
    if dp.exists(): words = {w.strip().lower() for w in dp.read_text(errors="ignore").splitlines()}
    pn = pathlib.Path("/usr/share/dict/propernames")
    if pn.exists(): proper = {w.strip() for w in pn.read_text(errors="ignore").splitlines()}
    phones, names, emps = collections.Counter(), collections.Counter(), collections.Counter()
    n_tr = 0
    for cf in sorted((ROOT / "data" / "raw").glob("*.csv")):
        for row in csv.DictReader(open(cf, newline="")):
            n_tr += 1; t = participant_text(row["text"])
            for m in ADDRESS.finditer(row["text"]):
                w = m.group(1) or m.group(2)
                if w in proper and w.lower() not in {"will", "mark", "grace", "rose", "hope", "joy", "bill", "art", "frank", "pat", "sue", "ray", "jack"}: names[w] += 1
            for m in PHONE.finditer(t): phones[m.group(0)] += 1
            for m in NAME_INTRO.finditer(t): names[m.group(1)] += 1
            for rx in (EMPLOYER, EMPLOYER2):
                for m in rx.finditer(t):
                    e = m.group(1).strip(" .,'")
                    if e and e.lower() not in STOP_EMP: emps[e] += 1
    # first names that stand alone: capitalised mid-sentence tokens in participant turns that are not dictionary words and not product-like
    mid = collections.Counter()
    for cf in sorted((ROOT / "data" / "raw").glob("*.csv")):
        for row in csv.DictReader(open(cf, newline="")):
            for m in re.finditer(r"(?<=[a-z,;] )([A-Z][a-z]{2,12})\b", participant_text(row["text"])):
                w = m.group(1)
                if w.lower() not in words: mid[w] += 1
    print(f"transcripts scanned {n_tr}; phone-like strings {len(phones)}; stated first names {len(names)}; employer phrases {len(emps)}; unusual capitalised words {len(mid)}")
    files = tracked(); blob = {f: f.read_text(errors="ignore") for f in files}
    if "--history" in sys.argv:   # also every line ever committed, on any branch
        blob = {ROOT / "(git history)": subprocess.run(["git", "log", "--all", "-p", "--no-color"], cwd=ROOT, capture_output=True, text=True, errors="ignore").stdout}
    hits = {}
    def look(kind, items, ci):
        found = collections.Counter()
        for it in items:
            if len(it) < 4 or it in ALLOW: continue
            rx = re.compile(r"(?<!\w)" + re.escape(it) + r"(?!\w)", re.I if ci else 0)
            for f, t in blob.items():
                if rx.search(t): found[f.relative_to(ROOT).as_posix()] += 1; hits.setdefault(kind, set()).add(it)
        return found
    res = {"phone": ("phone", look("phone", phones, False)), "stated first name": ("name", look("name", names, False)),
           "employer (any capitalisation)": ("employer", look("employer", emps, True)), "unusual capitalised word": ("cap", look("cap", mid, False))}
    bad = False
    for k, (key, c) in res.items():
        print(f"{k}: {len(hits.get(key, set()))} candidates occur in tracked files; files: {dict(c) if c else 'none'}")
        bad |= bool(c)
    if SHOW:
        for k, v in hits.items(): print(k, sorted(v))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
