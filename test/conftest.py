import sys
from pathlib import Path

# Agrega el directorio padre (raíz del proyecto) al PYTHONPATH
# Esto permite que pytest importe el paquete 'src' correctamente
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))