from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "source"
SCHEMA_YAML = SOURCE / "odph-v0.2" / "schema" / "change-package.yaml"
SCHEMA_JSON = SOURCE / "odph-v0.2" / "schema" / "change-package.json"
EXAMPLES_DIR = SOURCE / "examples"
PACKAGE_EXAMPLE = EXAMPLES_DIR / "retention-change" / "change-package.yaml"
OBJECTS_JSONL = SOURCE / "objects.jsonl"
LLMS_TXT = SOURCE / "llms.txt"
