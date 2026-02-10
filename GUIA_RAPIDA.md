# Guía Rápida: Azure Diagrams en 5 Minutos

## ⚡ TL;DR - Los Esenciales

```bash
# 1. Login en Azure
az login

# 2. Instala dependencias
pip install -r requirements.txt

# 3. Exporta tu infraestructura
python azure_export.py -s "YOUR-SUB-ID" -o infrastructure.json

# 4. Genera diagrama
python generate_network_flow_diagram_enhanced.py infrastructure.json

# 5. ¡Abre el PNG en diagrams/!
```

---

## 📦 Requisitos Mínimos

| Requisito | Instalación |
|-----------|------------|
| Python 3.8+ | `python --version` |
| GraphViz | `choco install graphviz` (Windows) |
| Azure CLI | `az login` |
| Python packages | `pip install -r requirements.txt` |

### ⚠️ NOTA IMPORTANTE PARA WINDOWS

En Windows, `graphviz2drawio` puede fallar al instalar (requiere compiladores C++).  
**Solución RECOMENDADA:** Usa Docker:

```bash
python run_diagram_enhanced_in_docker.py
```

Ver detalles en [GUIA_COMPLETA.md](./GUIA_COMPLETA.md) - Sección "Problema: graphviz2drawio"

---

## 🎯 Flujo Principal (3 pasos)

### 1️⃣ Exportar Azure
```bash
python azure_export.py -s "subscription-id" -o data.json
```
✅ Genera: `data.json`

### 2️⃣ Generar Diagrama
```bash
python generate_network_flow_diagram_enhanced.py data.json -o diagrama
```
✅ Genera: `diagrams/diagrama.png`, `.dot`, `.drawio`

### 3️⃣ Visualizar
- **PNG**: Abre directamente
- **DrawIO**: Upload a [draw.io](https://draw.io)
- **DOT**: Edita con editor de texto

---

## 🚀 Automatización

### Exportar Múltiples Suscripciones
Edita `run_exports.py` con tus subscription IDs:
```python
subscriptions = [
    ("id-1", "Producción"),
    ("id-2", "Desarrollo"),
]
```
Luego:
```bash
python run_exports.py
# ✅ Genera: exports/*.json
```

### Generar Múltiples Diagramas
```bash
python run_diagram_enhanced_in_docker.py
# ✅ Procesa todos los JSON en exports/ → diagrams/
```

---

## 🤖 Uso con IA

Usa [INSTRUCTIONS.md](./INSTRUCTIONS.md) como **megaprompt** para generar scripts personalizados:

```
Prompt para Claude/ChatGPT:

Lee estas instrucciones [COPIAR INSTRUCTIONS.md]

Ahora genera un script Python que cree diagramas que muestren [TU REQUISITO]
```

---

## 📊 Archivos de Salida

```
diagrams/
├── diagram.png      ← Imagen estática (para compartir)
├── diagram.dot      ← Código GraphViz (para versionado)
└── diagram.drawio   ← Editable (abre en draw.io)
```

---

## ⚠️ Solución Rápida de Problemas

| Problema | Solución |
|----------|----------|
| GraphViz not found | `winget install Graphviz.Graphviz` |
| JSON not found | `python azure_export.py -s "ID" -o file.json` |
| No subscriptions | `az login` |
| Archivo muy grande | Exporta suscripciones por separado |

---

## 💡 Comandos Clave

```bash
# Exportar
python azure_export.py -s "ID" -o infrastructure.json

# Diagrama básico
python generate_network_flow_diagram.py infrastructure.json

# Diagrama con NSGs (RECOMENDADO)
python generate_network_flow_diagram_enhanced.py infrastructure.json -o custom_name

# Múltiples exportaciones
python run_exports.py

# Múltiples diagramas (Docker)
python run_diagram_enhanced_in_docker.py
```

---

## 🔗 Recursos

- [Documentación completa](./GUIA_COMPLETA.md)
- [Instrucciones para IA](./INSTRUCTIONS.md)
- [Azure Python SDK](https://docs.microsoft.com/python/azure/)
- [Diagrams Library](https://diagrams.mingrammer.com/)
- [Draw.io](https://draw.io/)

---

**¿Necesitas más detalles?** Lee [GUIA_COMPLETA.md](./GUIA_COMPLETA.md)
