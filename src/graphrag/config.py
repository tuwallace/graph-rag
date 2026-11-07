"""Settings from environment / .env. No secrets in code."""
import os, pathlib
from dotenv import load_dotenv

ROOT = pathlib.Path(__file__).resolve().parents[2]
load_dotenv(ROOT / ".env")

RAW = ROOT / "data" / "raw"
SPLITS = ("workforce", "creatives", "scientists")

NEO4J_URI = os.getenv("NEO4J_URI", "bolt://localhost:7687")
NEO4J_USER = os.getenv("NEO4J_USER", "neo4j")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD", "")

OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434")
GEN_MODEL = os.getenv("GEN_MODEL", "qwen3:8b-16k")
EMBED_MODEL = os.getenv("EMBED_MODEL", "nomic-embed-text")
ROUTER_MODEL = os.getenv("ROUTER_MODEL", "nimble")
