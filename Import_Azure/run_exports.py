#!/usr/bin/env python3
"""
Exporta todas las suscripciones Azure a archivos JSON
"""
import subprocess
import os
from pathlib import Path

# Crear carpeta de salida
output_dir = Path("exports")
output_dir.mkdir(exist_ok=True)

# Suscripciones a exportar - REEMPLAZA CON TUS SUBSCRIPTION IDs
# Obtén los IDs con: az account list --query "[].id"
subscriptions = [
    ("xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx", "Production"),
    ("xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx", "Staging"),
    ("xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx", "Development"),
    # Agrega más suscripciones según sea necesario:
    # ("xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx", "QA"),
    # ("xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx", "NonProduction"),
]

print("Exportando todas las suscripciones...")
print()

for i, (sub_id, sub_name) in enumerate(subscriptions, 1):
    output_file = output_dir / f"{sub_name}.json"
    print(f"[{i}/10] {sub_name}")
    
    cmd = [
        "python",
        "azure_export.py",
        "-s", sub_id,
        "-o", str(output_file)
    ]
    
    try:
        subprocess.run(cmd, check=True)
        print(f"      ✓ Completado")
    except subprocess.CalledProcessError as e:
        print(f"      ✗ Error: {e}")
    
    print()

print("Proceso finalizado.")
print(f"Archivos guardados en: {output_dir.absolute()}")

# Listar archivos generados
files = list(output_dir.glob("*.json"))
if files:
    print("\nArchivos generados:")
    for file in sorted(files):
        size = file.stat().st_size / 1024
        print(f"  - {file.name} ({size:.2f} KB)")
