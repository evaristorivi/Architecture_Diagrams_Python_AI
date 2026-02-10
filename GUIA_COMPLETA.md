# Guía Completa: Azure Architecture Diagrams Generator

## 📋 Índice de Contenidos

1. [Visión General](#visión-general)
2. [Requisitos Previos](#requisitos-previos)
3. [Instalación de Dependencias](#instalación-de-dependencias)
4. [Flujo Completo del Proyecto](#flujo-completo-del-proyecto)
5. [Pasos Detallados](#pasos-detallados)
6. [Automatización](#automatización)
7. [Uso Avanzado con Prompts IA](#uso-avanzado-con-prompts-ia)
8. [Archivos de Salida](#archivos-de-salida)
9. [Troubleshooting](#troubleshooting)

---

## Visión General

Este proyecto permite **exportar la infraestructura de Azure a diagramas profesionales de topología de red** de manera automatizada. El flujo es el siguiente:

1. **Exportar infraestructura Azure** → Archivo JSON
2. **Generar diagramas de red** → PNG, DOT, DrawIO
3. **Opcionalmente**: Versión mejorada con NSG (Network Security Groups)

### Características Principales

✅ **Exportación automática** de toda tu infraestructura Azure  
✅ **Topología Hub-Spoke** automáticamente detectada  
✅ **Diagramas profesionales** con iconos reales de Azure  
✅ **Múltiples formatos** (PNG para visualización, DrawIO para edición, DOT para control de versiones)  
✅ **NSG visualización** (versión enhanced)  
✅ **IPs privadas de VMs** mostradas en los diagramas  
✅ **Automatización completa** con scripts Docker  
✅ **Integración con IA** para generar scripts personalizados  

---

## Requisitos Previos

Antes de comenzar, necesitas:

### 1. **Autenticación en Azure**

Debes estar autenticado en Azure CLI:

```bash
az login
```

Esto abre una ventana del navegador para que inicies sesión. Verifica que tengas:
- Acceso a las suscripciones Azure que deseas exportar
- Permisos de lectura en los recursos

### 2. **Python 3.8+**

Verifica la instalación:

```bash
python --version
# o en Linux/macOS
python3 --version
```

### 3. **GraphViz (Dependencia del Sistema)**

Es necesario para generar diagramas. Instálalo según tu SO:

**Windows:**
```bash
# Opción 1: Descargar desde https://graphviz.org/download/
# Opción 2: Con Chocolatey
choco install graphviz

# Opción 3: Con Winget
winget install Graphviz.Graphviz
```

**macOS:**
```bash
brew install graphviz
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt-get update
sudo apt-get install -y graphviz graphviz-dev build-essential python3-dev
```

**Verificar instalación:**
```bash
# Debería mostrar la ruta a GraphViz
which dot
# En Windows: where dot
```

### 4. **Docker (Opcional pero Recomendado)**

Para automatizar la generación de múltiples diagramas sin instalar dependencias locales:

```bash
docker --version
```

Descargable desde [Docker Desktop](https://www.docker.com/products/docker-desktop)

---

## Instalación de Dependencias

### Opción 1: Instalación Local (Recomendado)

```bash
# Navega a la carpeta del proyecto
cd Import_Azure

# Instala las dependencias de Python
pip install -r requirements.txt

# O instala solo lo necesario para diagramas
pip install -r requirements_diagram_generator.txt
```

### Opción 2: Instalación Modular (Por Etapas)

**Para exportar infraestructura:**
```bash
pip install azure-identity azure-core azure-common azure-mgmt-core
pip install azure-mgmt-network azure-mgmt-compute azure-mgmt-storage
pip install azure-mgmt-sql azure-mgmt-resource
```

**Para generar diagramas (SIN Docker):**
```bash
pip install diagrams graphviz>=0.20.3

# ⚠️ NOTA IMPORTANTE EN WINDOWS:
# graphviz2drawio requiere compiladores C++ y puede fallar
# Si solo quieres PNG y DOT, este paso es suficiente
pip install graphviz2drawio  # Opcional, ver nota abajo
```

**⚠️ Si estás en Windows y graphviz2drawio falla:**
Ver sección "Problema: graphviz2drawio command not found" en Troubleshooting.
La solución recomendada es usar Docker: `python run_diagram_enhanced_in_docker.py`

**Para análisis de infraestructura:**
```bash
# Usa solo librerías estándar de Python
# No requiere instalación adicional
```

### Opción 3: Entorno Virtual (Mejor Práctica)

```bash
# Crear entorno virtual
python -m venv venv

# Activar entorno
# En Windows:
venv\Scripts\activate
# En Linux/macOS:
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt
```

---

## Flujo Completo del Proyecto

```
┌─────────────────────────────────────────────────────────────────┐
│                      FLUJO GENERAL                              │
└─────────────────────────────────────────────────────────────────┘

1. EXPORTACIÓN AZURE
   python azure_export.py -s <subscription_id> -o infrastructure.json
   └─> Crea: infrastructure.json (en raíz o carpeta exports/)

2. GENERACIÓN DE DIAGRAMAS (Versión Básica)
   python generate_network_flow_diagram.py infrastructure.json
   └─> Crea en diagrams/:
       - diagram_1.png (visualización estática)
       - diagram_1.dot (código GraphViz)
       - diagram_1.drawio (editable)

3. GENERACIÓN DE DIAGRAMAS (Versión Enhanced con NSGs)
   python generate_network_flow_diagram_enhanced.py infrastructure.json
   └─> Crea los mismos formatos + soporte para NSGs

┌─────────────────────────────────────────────────────────────────┐
│                  FLUJO CON AUTOMATIZACIÓN                       │
└─────────────────────────────────────────────────────────────────┘

1. EXPORTACIÓN MÚLTIPLE (Automatizada)
   python run_exports.py
   └─> Exporta TODAS las suscripciones
   └─> Crea: exports/*.json

2. GENERACIÓN DE DIAGRAMAS MÚLTIPLES
   Opción A: python run_diagram_in_docker.py
   Opción B: python run_diagram_enhanced_in_docker.py
   └─> Procesa todos los JSON de exports/
   └─> Crea múltiples diagramas en diagrams/
```

---

## Pasos Detallados

### Paso 1: Exportar Infraestructura Azure

#### Opción A: Exportar Suscripción Individual

```bash
python azure_export.py -s "tu-subscription-id" -o infrastructure.json
```

**Argumentos disponibles:**
```
-s, --subscriptions  ID de la suscripción Azure (requerido)
-o, --output         Nombre del archivo JSON de salida (por defecto: azure-infrastructure.json)
--count              Mostrar conteo de recursos exportados
```

**Ejemplo completo:**
```bash
# Obtén el ID de tu suscripción con: az account show --query id -o tsv
python azure_export.py \
  -s "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx" \
  -o "mi_suscripcion.json" \
  --count
```

**Salida esperada:**
```
✓ Loading subscriptions...
✓ 1 subscription(s) ready
✓ Processing subscription: My Subscription ID

✓ 📦 Exporting 45 VMs
✓ 📦 Exporting 12 Virtual Networks
✓ 📦 Exporting 8 Load Balancers
✓ 📦 Exporting 5 SQL Servers
...

✅ Export completado
📄 JSON guardado en: infrastructure.json (2.5 MB)
```

#### Opción B: Exportar Múltiples Suscripciones (Automatizado)

Edita `run_exports.py` con tus suscripciones:

```python
# Obtén los IDs con: az account list --query "[].id"
subscriptions = [
    ("xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx", "Production"),
    ("xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx", "Development"),
    ("xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx", "QA"),
]
```

Luego ejecuta:
```bash
python run_exports.py
```

**Resultado:**
```
exports/
├── Production.json (2.3 MB)
├── Development.json (1.8 MB)
└── QA.json (1.5 MB)
```

---

### Paso 2: Generar Diagramas de Red

#### Opción A: Versión Básica

Para crear diagramas simples de topología de red:

```bash
python generate_network_flow_diagram.py infrastructure.json
```

**Argumentos:**
```bash
python generate_network_flow_diagram.py <archivo_json> [-o nombre_salida]
```

**Ejemplo:**
```bash
python generate_network_flow_diagram.py exports/Production.json -o diagrama_prod
```

**Salida:**
```
diagrams/
├── diagrama_prod.png (imagen estática)
├── diagrama_prod.dot (código GraphViz)
└── diagrama_prod.drawio (archivo editable)
```

#### Opción B: Versión Enhanced (Recomendado)

Incluye visualización de NSGs, IPs privadas de VMs, y más detalles:

```bash
python generate_network_flow_diagram_enhanced.py infrastructure.json
```

**Características adicionales:**
- ✅ NSGs mostrados a nivel de subred y NIC
- ✅ IPs privadas de VMs en los nodos
- ✅ Mejor visualización de Private Endpoints
- ✅ Resumen de reglas de seguridad

**Ejemplo completo:**
```bash
python generate_network_flow_diagram_enhanced.py \
  exports/Produccion.json \
  -o diagrama_produccion_enhanced
```

---

### Paso 3: (Opcional) Personalizar con IA

El archivo [INSTRUCTIONS.md](Import_Azure/INSTRUCTIONS.md) contiene un **megaprompt** para la IA que describe exactamente cómo generar scripts de diagrama.

#### Usa el megaprompt como base:

1. **Copia el contenido de INSTRUCTIONS.md**
2. **Copia tu archivo JSON de exportación**
3. **Proporciona ambos a Claude, ChatGPT o tu herramienta IA favorita**
4. **Solicita:** "Based on these instructions and this Azure export, generate a Python script to create diagrams with [tu característica específica]"

**Ejemplo de prompt personalizado:**

```
Lee el archivo INSTRUCTIONS.md que es un megaprompt para generar Python scripts
de diagramas de red Azure. 

Basándote en este megaprompt y la estructura del JSON de exports/Produccion.json,
crea un nuevo generador de diagramas que:

1. Muestre las NSGs con colores diferentes según el tipo de regla (ingress/egress)
2. Agrupe las VMs por función (web, app, database)
3. Agregue información de puertos abiertos en las reglas NSG

Genera el script Python completo.
```

#### Edita el megaprompt si es necesario:

Si deseas personalizar la forma en que se generan los diagramas, modifica [INSTRUCTIONS.md](Import_Azure/INSTRUCTIONS.md) con tus requisitos específicos.

---

## Automatización

### Automatización Local: Generar Múltiples Diagramas

Si tienes muchos JSON en la carpeta `exports/`, usa los scripts de automatización:

#### Versión básica:
```bash
python run_diagram_in_docker.py
```

#### Versión enhanced:
```bash
python run_diagram_enhanced_in_docker.py
```

**Esto genera diagramas para TODOS los JSON en exports/**

### Requisitos para Automatización:

- Docker instalado y en ejecución
- Archivos JSON en carpeta `exports/`
- Eso es todo - Docker maneja el resto de dependencias

### Proceso Automatizado Completo

**Script de ejemplo que realiza TODO:**

```bash
#!/bin/bash

# 1. Exportar todas las suscripciones
echo "📤 Exportando infraestructura..."
python run_exports.py

# 2. Generar diagramas enhanced
echo "📊 Generando diagramas..."
python run_diagram_enhanced_in_docker.py

# 3. Mostrar resultados
echo "✅ Diagramas generados en diagrams/"
ls -lh diagrams/
```

Guarda esto como `pipeline.sh` y ejecuta:
```bash
chmod +x pipeline.sh
./pipeline.sh
```

---

## Uso Avanzado con Prompts IA

### Cómo Usar INSTRUCTIONS.md como Megaprompt

El archivo [INSTRUCTIONS.md](Import_Azure/INSTRUCTIONS.md) es un **megaprompt completo** para IA que describe:

1. **Arquitectura de la solución**
2. **Estructura de datos del JSON**
3. **Cómo procesar la información**
4. **Cómo generar diagramas profesionales**
5. **Patrones y mejores prácticas**

#### Pasos para Personalización:

**1. Abre INSTRUCTIONS.md en tu editor IA favorito**

```markdown
# Agent Instructions: Azure Network Flow Diagram Generation

You are tasked with generating a professional network flow diagram...
```

**2. Modifica las secciones según tus necesidades:**

```markdown
## Personalizaciones Solicitadas

- Agregar visualización de Tags de Azure
- Mostrar costos estimados por recurso
- Diferenciar recursos por criticidad
```

**3. Usa el prompt personalizado con TODAS tus instrucciones**

#### Ejemplo de Prompt Completo:

```plaintext
Eres un experto en Python y Azure.

Lee y comprende completamente el siguiente megaprompt que describe 
cómo generar diagramas de topología de red Azure:

[COPIAR TODO EL CONTENIDO DE INSTRUCTIONS.md]

Ahora, crea un nuevo script Python llamado:
generate_network_flow_with_costs.py

Que tome un JSON de exportación Azure y genere diagramas que muestren:

1. Topología de red (como de costumbre)
2. Costos estimados por recurso (azul oscuro = caro, verde = barato)
3. Tags y etiquetas de Azure
4. Marcar recursos en "Deprecated" con un ícono especial

Genera el script completo y funcional, listo para usar.

JSON de entrada será de este formato:
[COPIAR UN EJEMPLO DEL TU JSON DE EXPORTACIÓN]
```

### Mejores Prácticas de Prompts

| Acción | Resultado |
|--------|-----------|
| ✅ Incluir INSTRUCTIONS.md completo | Scripts personalizados funcionales |
| ✅ Proporcionar ejemplo JSON | IA entiende la estructura |
| ✅ Detallar casos específicos | Maneja excepciones correctamente |
| ❌ Prompts vagos | Scripts incompletos o no funcionales |
| ❌ Sin ejemplos | Asunciones incorrectas |

---

## Archivos de Salida

### Carpeta `exports/`

Contiene archivos JSON exportados de Azure:

```
exports/
├── Produccion.json (exportación de suscripción completa)
├── Development.json
├── QA.json
└── ... (más suscripciones)
```

**Estructura del JSON:**
```json
{
  "subscriptions": [
    {
      "subscriptionId": "...",
      "displayName": "Produccion",
      "resourceGroups": [
        {
          "resourceGroupName": "rg-web",
          "resources": {
            "network": {
              "virtualNetworks": [...],
              "networkInterfaces": [...],
              "networkSecurityGroups": [...]
            },
            "compute": {
              "virtualMachines": [...],
              "virtualMachineScaleSets": [...]
            },
            "sql": { "servers": [...] },
            "storage": { "storageAccounts": [...] },
            "keyvault": { "vaults": [...] }
          }
        }
      ]
    }
  ]
}
```

### Carpeta `diagrams/`

Contiene los diagramas generados (3 formatos por archivo):

```
diagrams/
├── diagram_Produccion.png (imagen estática, para ver/compartir)
├── diagram_Produccion.dot (código GraphViz, para versionado)
├── diagram_Produccion.drawio (editable en Draw.io)
├── diagram_Development.png
├── diagram_Development.dot
├── diagram_Development.drawio
└── ...
```

#### Formato PNG
- **Uso**: Presentaciones, documentación, Slack
- **Abre con**: Cualquier visor de imágenes
- **Editable**: No (genera con DrawIO para editar)

#### Formato DrawIO
- **Uso**: Edición, anotaciones, personalizaciones
- **Abre con**: [draw.io](https://draw.io) o importa en yEd, Lucidchart
- **Editable**: Sí, totalmente

#### Formato DOT
- **Uso**: Control de versiones, CI/CD, automatización
- **Formato**: Texto plano (GraphViz)
- **Editable**: Sí, con cualquier editor de texto

---

## Troubleshooting

### Problema: "GraphViz not found"

**Causa**: GraphViz no está instalado o no está en PATH

**Solución:**

```bash
# Windows
# 1. Descarga desde https://graphviz.org/download/
# 2. Durante instalación, marca "Add Graphviz to PATH"
# 3. Reinicia Command Prompt/PowerShell

# O usa:
winget install Graphviz.Graphviz

# Verifica:
dot -V
```

**Si sigue sin funcionar:**
```bash
# Windows: Agrega manualmente a PATH en Python
import os
os.environ['PATH'] += r';C:\Program Files\Graphviz\bin'
```

### Problema: "File not found: azure-infrastructure.json"

**Causa**: El archivo JSON no se generó o está en otra carpeta

**Solución:**
```bash
# Primero exporta la infraestructura
python azure_export.py -s "tu-subscription-id" -o infrastructure.json

# Verifica que el archivo existe
ls infrastructure.json
# En Windows: dir infrastructure.json

# Luego genera el diagrama
python generate_network_flow_diagram.py infrastructure.json
```

### Problema: "AzureCliCredential: No subscriptions found"

**Causa**: No estás autenticado en Azure o no tienes suscripciones

**Solución:**
```bash
# Inicia sesión en Azure
az login

# Selecciona la suscripción correcta
az account set --subscription "id-de-suscripcion"

# Verifica que tienes suscripciones
az account list
```

### Problema: "graphviz2drawio command not found" o error en compilación (⚠️ ESPECIALMENTE EN WINDOWS)

**Causa**: 
- En **Windows**: `graphviz2drawio` requiere compilación C/C++ y puede fallar debido a falta de build tools
- En **macOS/Linux**: Generalmente se instala sin problemas

**Síntomas comunes en Windows:**
```
error: Microsoft Visual C++ 14.0 or greater is required
build failed
failed building wheel for graphviz2drawio
```

**Solución A: Para Windows (RECOMENDADO - Usar Docker)**

En lugar de instalar `graphviz2drawio` localmente, usa los scripts Docker que ya lo incluyen:

```bash
# NO ejecutar:
# pip install graphviz2drawio  ❌ NO en Windows

# EJECUTAR en cambio:
python run_diagram_in_docker.py
# O para versión enhanced:
python run_diagram_enhanced_in_docker.py
```

**Por qué funciona Docker:**
- Docker levanta un entorno Linux dentro de Windows
- En Linux, `graphviz2drawio` se compila correctamente
- No necesitas instalar build tools de C++ localmente
- Perfecto para automatizar múltiples exportaciones también

**Ventaja adicional:** Si tienes múltiples JSONs (múltiples suscripciones), `run_diagram_*_in_docker.py` procesa todos automáticamente.

**Solución B: Para Windows (Si NECESITAS local sin Docker)**

Instala Visual C++ build tools:
1. Descargar: [Microsoft C++ Build Tools](https://visualstudio.microsoft.com/visual-cpp-build-tools/)
2. Instalar con opción "Desktop development with C++"
3. Reiniciar CMD/PowerShell
4. Luego:
```bash
pip install --upgrade setuptools wheel
pip install graphviz2drawio
```

**Solución C: Ignorar DrawIO (Si falla todo)**

La conversión a `.drawio` es opcional. Los scripts generan:
- ✅ PNG (imagen, abre directamente)
- ✅ DOT (código GraphViz, editable)
- ❌ DrawIO (falla en Windows sin herramientas)

Puedes trabajar sin el formato DrawIO:
```bash
# Si falla graphviz2drawio, aún tendrás PNG y DOT
python generate_network_flow_diagram_enhanced.py infrastructure.json
# Resultado: archivo.png y archivo.dot funcionan
# El archivo.drawio podría fallar, pero no es crítico
```

**RECOMENDACIÓN FINAL PARA WINDOWS:**
```
┌─────────────────────────────────────────┐
│  Opción 1: USA DOCKER (RECOMENDADO)     │
│  python run_diagram_enhanced_in_docker.py │
│                                          │
│  Ventajas:                              │
│  ✓ Funciona 100% en Windows             │
│  ✓ Procesa múltiples JSONs              │
│  ✓ No requiere build tools              │
│  ✓ Más rápido que instalar localmente   │
└─────────────────────────────────────────┘
```

### Problema: Docker error en run_diagram_in_docker.py

**Causa**: Docker no está corriendo o no está instalado

**Solución:**
```bash
# Opción 1: Instala Docker
# Descarga Docker Desktop: https://www.docker.com/products/docker-desktop

# Opción 2: Usa generación local (sin Docker)
# ⚠️ NOTA IMPORTANTE EN WINDOWS:
# graphviz2drawio puede fallar en Windows (requiere compiladores C++)
# Por eso Docker es la solución recomendada

python generate_network_flow_diagram_enhanced.py exports/*.json

# Si graphviz2drawio falla, aún generarás:
# ✅ PNG (imagen estática)
# ✅ DOT (código GraphViz)
# ⚠️ DrawIO (puede fallar en Windows sin build tools)
```

### Problema: JSON muy grande (>10MB)

**Causa**: Exportación de infraestructura muy grande

**Solución:**
```bash
# Exporta por suscripción individual
python azure_export.py -s "sub-1" -o sub1.json
python azure_export.py -s "sub-2" -o sub2.json

# Genera diagramas por separado
python generate_network_flow_diagram_enhanced.py sub1.json -o diagrama_sub1
python generate_network_flow_diagram_enhanced.py sub2.json -o diagrama_sub2
```

### Problema: Memoria insuficiente al generar diagramas

**Causa**: Infraestructura muy grande con muchos recursos

**Solución:**
```bash
# Usa la versión en Docker (mejor manejo de recursos)
python run_diagram_enhanced_in_docker.py

# O aumenta memoria disponible
docker update --memory=4g [container_id]
```

### Problema: NSGs no se muestran en la versión enhanced

**Causa**: El JSON no contiene NSGs o están mal estructurados

**Solución:**
```bash
# Verifica que el JSON contiene NSGs
python -c "
import json
with open('infrastructure.json') as f:
    data = json.load(f)
    for sub in data['subscriptions']:
        for rg in sub['resourceGroups']:
            nsgs = rg['resources'].get('network', {}).get('networkSecurityGroups', [])
            print(f'NSGs encontrados: {len(nsgs)}')
"
```

---

## Resumen de Comandos Básicos

```bash
# 1. EXPORTAR INFRAESTRUCTURA
python azure_export.py -s "YOUR-SUBSCRIPTION-ID" -o infrastructure.json

# 2. GENERAR DIAGRAMA (Básico)
python generate_network_flow_diagram.py infrastructure.json

# 3. GENERAR DIAGRAMA (Enhanced con NSGs) ⭐ Recomendado
python generate_network_flow_diagram_enhanced.py infrastructure.json -o mi_diagrama

# 4. AUTOMATIZAR EXPORTACIÓN MÚLTIPLE
python run_exports.py

# 5. AUTOMATIZAR GENERACIÓN (Múltiples diagramas)
python run_diagram_enhanced_in_docker.py

# 6. VER DIAGRAMAS GENERADOS
# PNG: Abre directamente
# DrawIO: Sube a https://draw.io o abre en aplicación
# DOT: Edita con cualquier editor de texto
```

---

## Próximos Pasos

1. ✅ **Autentica en Azure** (`az login`)
2. ✅ **Instala dependencias** (`pip install -r requirements.txt`)
3. ✅ **Exporta tu infraestructura** (`python azure_export.py -s ...`)
4. ✅ **Genera diagramas** (`python generate_network_flow_diagram_enhanced.py ...`)
5. ✅ **Visualiza los resultados** en `diagrams/`
6. ✅ **(Opcional) Personaliza con prompts IA** usando INSTRUCTIONS.md

---

## Contacto y Soporte

- **Issues con Azure SDK**: Consulta [Azure Python SDK docs](https://docs.microsoft.com/python/azure/)
- **Issues con diagrams**: Consulta [mingrammer/diagrams](https://diagrams.mingrammer.com/)
- **Issues con GraphViz**: Consulta [GraphViz official docs](https://graphviz.org/documentation/)
- **Issues con Docker**: Consulta [Docker documentation](https://docs.docker.com/)

---

**Última actualización**: Febrero 2026  
**Versión**: 1.0.0
