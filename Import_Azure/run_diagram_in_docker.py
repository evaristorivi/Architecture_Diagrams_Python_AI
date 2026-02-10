#!/usr/bin/env python3
# --------------------------------
# Ejecuta generate_network_flow_diagram.py en Docker con GraphViz
# Procesa múltiples archivos JSON desde la carpeta exports/
# Evaristo R. Rivieccio Vega
# --------------------------------
import os
import subprocess
import shutil
import sys
from pathlib import Path

# Configuración
DOCKER_WORK_DIR = "/workspace"
LOCAL_WORK_DIR = os.path.abspath(".")
SCRIPT_FILE = "generate_network_flow_diagram"
EXPORTS_DIR = "exports"
DIAGRAMS_DIR = "diagrams"

# Crear directorio de salida si no existe
os.makedirs(DIAGRAMS_DIR, exist_ok=True)

# Encontrar todos los JSON en la carpeta exports/
exports_path = Path(EXPORTS_DIR)
if not exports_path.exists():
    print(f"❌ Carpeta no encontrada: {EXPORTS_DIR}")
    sys.exit(1)

json_files = sorted(list(exports_path.glob("*.json")))
if not json_files:
    print(f"❌ No se encontraron archivos .json en {EXPORTS_DIR}")
    sys.exit(1)

print(f"📁 Se procesarán {len(json_files)} archivos JSON:")
for f in json_files:
    print(f"   • {f.name}")

# Crear script bash compatible con Linux (saltos de línea '\n')
bash_script = f"""#!/bin/bash
set -e
echo "📦 Instalando dependencias del sistema..."
apt-get update
apt-get install -y graphviz graphviz-dev build-essential python3-dev

echo "🐍 Instalando paquetes Python..."
pip install --upgrade pip
pip install graphviz2drawio diagrams azure-identity azure-core azure-mgmt-network azure-mgmt-compute azure-mgmt-storage

echo "🎨 Ejecutando generador de diagramas para múltiples JSON..."
cd {DOCKER_WORK_DIR}

for json_file in {EXPORTS_DIR}/*.json; do
    filename=$(basename "$json_file")
    basename_no_ext="${{filename%.*}}"
    output_name="diagram_${{basename_no_ext}}"
    
    echo ""
    echo "   📊 Procesando: $filename -> $output_name"
    python generate_network_flow_diagram.py "$json_file" -o "$output_name"
done

echo ""
echo "✅ Todos los diagramas generados en el contenedor"
"""

# Escribir script con saltos de línea Unix
with open(SCRIPT_FILE, "w", encoding="utf-8", newline="\n") as f:
    f.write(bash_script)

# Ejecutar Docker
docker_cmd = [
    "docker", "run", "--rm",
    "-v", f"{LOCAL_WORK_DIR}:{DOCKER_WORK_DIR}",
    "python:3.10-slim",
    "bash", f"{DOCKER_WORK_DIR}/{SCRIPT_FILE}"
]

print("\n" + "=" * 60)
print("🐳 Ejecutando diagramas en Docker para múltiples JSON...")
print("=" * 60)

try:
    subprocess.check_call(docker_cmd)
    print("\n" + "=" * 60)
    print("✅ ¡Completado!")
    print("=" * 60)
    print(f"\n📁 Archivos generados en {DIAGRAMS_DIR}/:")
    diagrams_dir = Path(DIAGRAMS_DIR)
    if diagrams_dir.exists():
        files = sorted(diagrams_dir.glob("diagram_*"))
        if files:
            for f in files:
                print(f"   ✅ {f.name}")
        else:
            print("   ⚠️  No se encontraron archivos nuevos")
except subprocess.CalledProcessError as e:
    print(f"\n❌ Error al ejecutar Docker: {e}")
    sys.exit(1)
except FileNotFoundError:
    print("\n❌ Docker no está instalado o no está en el PATH")
    sys.exit(1)
finally:
    # Limpiar script temporal
    if os.path.exists(SCRIPT_FILE):
        os.remove(SCRIPT_FILE)
