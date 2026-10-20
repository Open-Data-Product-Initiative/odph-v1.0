from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "source"
SCHEMA_YAML = SOURCE / "odph-v0.2" / "schema" / "kentaro-change.yaml"
SCHEMA_JSON = SOURCE / "odph-v0.2" / "schema" / "kentaro-change.json"
EXAMPLES_DIR = SOURCE / "examples"
OBJECTS_JSONL = SOURCE / "objects.jsonl"
LLMS_TXT = SOURCE / "llms.txt"
