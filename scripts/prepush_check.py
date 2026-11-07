"""Pre-push check (ADR-0012). Fails when a tracked file could expose the transcript corpus or a secret.
  1. no tracked path under data/ or named .env (only .env.example is allowed)
  2. no tracked file over 1 MB
  3. no tracked text file shares a run of MAX_RUN words with the corpus in data/raw (a sentence-length excerpt is allowed, a paragraph is not)
  4. gitleaks finds no secrets in the tracked files (skipped with a warning if gitleaks is not installed)
Run: uv run python scripts/prepush_check.py        Exit code 0 = clean.
"""
import csv, pathlib, re, shutil, subprocess, sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
MAX_RUN = 25          # words; ADR-0012 allows short attributed excerpts, "more than a sentence" is not allowed
SIZE_LIMIT = 1_000_000
TEXT_SUFFIX = {".md", ".py", ".json", ".yml", ".yaml", ".toml", ".txt", ".cfg", ".example", ".sh", ""}
WORD = re.compile(r"[a-z0-9']+")


def tracked() -> list[pathlib.Path]:
    out = subprocess.run(["git", "ls-files", "-z"], cwd=ROOT, capture_output=True, check=True).stdout.decode().split("\0")
    return [ROOT / p for p in out if p]


def shingles(words: list[str], n: int):
    for i in range(len(words) - n + 1):
        yield hash(" ".join(words[i:i + n]))


def main() -> int:
    problems = []
    files = tracked()
    for p in files:
        rel = p.relative_to(ROOT).as_posix()
        if rel.startswith("data/") or rel == ".env" or rel.startswith(".env.") and rel != ".env.example":
            problems.append(f"tracked path not allowed: {rel}")
        elif p.exists() and p.stat().st_size > SIZE_LIMIT:
            problems.append(f"file over 1 MB: {rel}")
    # corpus overlap
    raw = ROOT / "data" / "raw"
    corpus_files = sorted(raw.glob("*.csv")) if raw.exists() else []
    if not corpus_files:
        print("WARNING: data/raw not present; corpus-overlap check skipped (run scripts/download_data.py to enable it)")
    else:
        mine = {}   # shingle hash -> (file, first word index)
        for p in files:
            if p.suffix in TEXT_SUFFIX and p.exists() and p.stat().st_size < SIZE_LIMIT:
                w = WORD.findall(p.read_text(errors="ignore").lower())
                for h in shingles(w, MAX_RUN):
                    mine.setdefault(h, p.relative_to(ROOT).as_posix())
        csv.field_size_limit(10**9)
        hit = {}
        for cf in corpus_files:
            for row in csv.DictReader(open(cf, newline="")):
                for h in shingles(WORD.findall(row["text"].lower()), MAX_RUN):
                    if h in mine:
                        hit.setdefault(mine[h], row["transcript_id"])
        problems += [f"shares a run of {MAX_RUN}+ words with the corpus: {f} (e.g. {t})" for f, t in sorted(hit.items())]
    # gitleaks
    if shutil.which("gitleaks"):
        scans = [["gitleaks", "git", str(ROOT), "--staged", "--no-banner", "--redact"]]            # what is about to be committed
        if subprocess.run(["git", "rev-parse", "--verify", "-q", "HEAD"], cwd=ROOT, capture_output=True).returncode == 0:
            scans.append(["gitleaks", "git", str(ROOT), "--no-banner", "--redact", "--log-opts=--all"])   # every commit already made
        for cmd in scans:
            r = subprocess.run(cmd, capture_output=True, text=True)
            if r.returncode != 0:
                problems.append("gitleaks reported findings (" + " ".join(cmd[2:3] + cmd[3:4]) + "):\n" + (r.stdout + r.stderr)[-1500:])
    else:
        print("WARNING: gitleaks not installed; secret scan skipped")
    for m in problems:
        print("FAIL:", m)
    print(f"checked {len(files)} tracked files; {'FAILED' if problems else 'clean'}")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
