#!/usr/bin/env python3
# --------------------------------
# Ejecuta generate_network_flow_diagram_enhanced.py en Docker con GraphViz
# Procesa múltiples archivos JSON desde la carpeta exports/
# Versión ENHANCED con soporte completo para NSGs a nivel subnet y NIC
# --------------------------------
import os
import subprocess
import shutil
import sys
from pathlib import Path

# Configuración
DOCKER_WORK_DIR = "/workspace"
LOCAL_WORK_DIR = os.path.abspath(".")
SCRIPT_FILE = "generate_network_flow_diagram_enhanced"
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

echo "🎨 Ejecutando generador de diagramas ENHANCED para múltiples JSON..."
cd {DOCKER_WORK_DIR}

# Establecer encoding UTF-8
export PYTHONIOENCODING=utf-8

for json_file in {EXPORTS_DIR}/*.json; do
    filename=$(basename "$json_file")
    basename_no_ext="${{filename%.*}}"
    output_name="diagram_${{basename_no_ext}}"
    
    echo ""
    echo "   📊 Procesando: $filename -> $output_name"
    python generate_network_flow_diagram_enhanced.py "$json_file" -o "$output_name"
done

echo ""
echo "✅ Todos los diagramas generados (ENHANCED) en el contenedor"
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
print("🐳 Ejecutando en Docker...")
print("=" * 60 + "\n")

try:
    result = subprocess.run(docker_cmd, check=True)
except subprocess.CalledProcessError as e:
    print(f"❌ Error en Docker: {e}")
    sys.exit(1)
except FileNotFoundError:
    print("❌ Docker no está instalado o no está en PATH")
    sys.exit(1)

# Resumen de salida
print("\n" + "=" * 60)
print("✅ ¡Completado!")
print("=" * 60 + "\n")

diagram_files = sorted(list(Path(DIAGRAMS_DIR).glob("diagram_*.dot")))
if diagram_files:
    print(f"📁 Archivos generados en {DIAGRAMS_DIR}/:")
    for f in diagram_files:
        stem = f.stem  # diagram_XYZ
        dot_file = f
        png_file = f.with_suffix(".png")
        drawio_file = f.with_suffix(".drawio")
        
        if dot_file.exists():
            print(f"   ✅ {dot_file.name}")
        if png_file.exists():
            print(f"   ✅ {png_file.name}")
        if drawio_file.exists():
            print(f"   ✅ {drawio_file.name}")
else:
    print("⚠️  No se encontraron archivos generados")
