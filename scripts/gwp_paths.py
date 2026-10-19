from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "source"
SCHEMA_YAML = SOURCE / "schema" / "gwp.yaml"
SCHEMA_JSON = SOURCE / "schema" / "gwp.json"
EXAMPLES_DIR = SOURCE / "examples"
OBJECTS_JSONL = SOURCE / "objects.jsonl"
LLMS_TXT = SOURCE / "llms.txt"
