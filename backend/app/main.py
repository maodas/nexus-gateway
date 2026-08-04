"""
App package entrypoint alias for uvicorn app.main:app invocation.
"""
import sys
from pathlib import Path

# Add backend directory to python path if invoking via app.main
backend_dir = Path(__file__).resolve().parent.parent
if str(backend_dir) not in sys.path:
    sys.path.insert(0, str(backend_dir))

from main import app  # noqa: F401
