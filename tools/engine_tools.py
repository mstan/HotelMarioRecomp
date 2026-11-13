"""Import reusable debug/provenance tools from the pinned engine checkout."""
import os
from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parents[1]
ENGINE = Path(os.environ.get("CDIRECOMP_ROOT", ROOT / "cdirecomp")).resolve()
sys.path.insert(0, str(ENGINE / "tools"))
