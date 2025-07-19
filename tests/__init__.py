"""Tests unitaires.

Assure que le dossier racine du projet est présent dans le ``PYTHONPATH`` afin
de pouvoir importer correctement le package ``appointment_agent`` lors de
l'exécution des tests.
"""

import sys
from pathlib import Path

root_path = Path(__file__).resolve().parents[1]
if str(root_path) not in sys.path:
    sys.path.insert(0, str(root_path))
