import os
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent

# -----------------------------------------------------------------------------
# DATA_DIR / DATABASE_DIR can be overridden via environment variables.
# Locally, these env vars are not set, so behavior is IDENTICAL to before
# (falls back to PROJECT_ROOT / "data" and PROJECT_ROOT / "database").
#
# On Render, we set DATA_DIR and DATABASE_DIR to point to the mounted
# persistent disk so the SQLite database survives restarts/redeploys.
# -----------------------------------------------------------------------------

DATA_DIR = Path(os.getenv("DATA_DIR", str(PROJECT_ROOT / "data")))
DATABASE_DIR = Path(os.getenv("DATABASE_DIR", str(PROJECT_ROOT / "database")))

DATA_DIR.mkdir(parents=True, exist_ok=True)
DATABASE_DIR.mkdir(parents=True, exist_ok=True)



















# from pathlib import Path


# PROJECT_ROOT = Path(__file__).resolve().parent.parent
# DATA_DIR = PROJECT_ROOT / "data"
# DATABASE_DIR = PROJECT_ROOT / "database"

# DATA_DIR.mkdir(exist_ok=True)
# DATABASE_DIR.mkdir(exist_ok=True)