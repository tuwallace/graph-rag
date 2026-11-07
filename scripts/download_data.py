"""Download the Anthropic/AnthropicInterviewer transcripts into data/raw/{workforce,creatives,scientists}.csv (git-ignored).
Source: https://huggingface.co/datasets/Anthropic/AnthropicInterviewer (see README for attribution and license notes).
Run: uv run python scripts/download_data.py
"""
import pathlib, sys, urllib.request, csv

BASE = "https://huggingface.co/datasets/Anthropic/AnthropicInterviewer/resolve/main/interview_transcripts/{}_transcripts.csv"
RAW = pathlib.Path(__file__).resolve().parents[1] / "data" / "raw"
EXPECT = {"workforce": 1000, "creatives": 125, "scientists": 125}

def main():
    RAW.mkdir(parents=True, exist_ok=True); csv.field_size_limit(10**9)
    for split, n in EXPECT.items():
        dest = RAW / f"{split}.csv"
        if not dest.exists():
            print("downloading", split, flush=True)
            urllib.request.urlretrieve(BASE.format(split), dest)
        with open(dest, newline="") as f:
            rows = list(csv.DictReader(f))
        assert rows and set(rows[0]) >= {"transcript_id", "text"}, f"{dest}: unexpected columns"
        print(f"{split}: {len(rows)} transcripts" + ("" if len(rows) == n else f" (expected {n})"))

if __name__ == "__main__":
    sys.exit(main())
