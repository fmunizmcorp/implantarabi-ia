import os
import sys

RAIZ = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
if RAIZ not in sys.path:
    sys.path.insert(0, RAIZ)
