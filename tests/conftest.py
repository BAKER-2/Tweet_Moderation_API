
import os, sys
# Add project root (one level up from tests/) to sys.path so 'app' is importable
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)
