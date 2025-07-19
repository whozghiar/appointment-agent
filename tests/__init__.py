"""Tests unitaires.

Ajoute le dossier ``src`` au ``PYTHONPATH`` pour permettre les imports du
package ``appointment_agent`` durant l'exécution des tests.
"""

import sys
from pathlib import Path

src_path = Path(__file__).resolve().parents[1] / "src"
if str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))
