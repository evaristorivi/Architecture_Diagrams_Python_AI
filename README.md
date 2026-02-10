# Architecture Diagrams Generator using Python and AI

## 📺 Video Tutorials

### Step by Step Details - New Azure Environment

[![Video Title](https://img.youtube.com/vi/m7EuZ7GhinE/0.jpg)](https://www.youtube.com/watch?v=m7EuZ7GhinE)

### Step by Step Details - Existing Azure Environment

[![Video Title](https://img.youtube.com/vi/E-1RiX8DvRI/0.jpg)](https://www.youtube.com/watch?v=E-1RiX8DvRI)

---

## 📦 Descripción del Proyecto

**Azure Architecture Diagrams Generator** es una suite de herramientas Python que permite:

1. **Exportar** automáticamente la infraestructura Azure a archivos JSON
2. **Analizar** la infraestructura exportada
3. **Generar** diagramas profesionales de topología de red
4. **Automatizar** el proceso para múltiples suscripciones/infraestructuras

---

## 📂 Estructura del Proyecto

```
Raíz del Proyecto (START HERE!)
├── 📄 INDICE_DOCUMENTACION.md          ⭐ Lee esto primero
├── 📄 GUIA_RAPIDA.md                   ⚡ 5 minutos
├── 📄 GUIA_COMPLETA.md                 📖 Documentación exhaustiva
├── 📄 MATRIZ_REQUISITOS.md             ✅ Checklist de requisitos
├── 📄 WINDOWS_GRAPHVIZ_SOLUTION.md     🪟 Solución Windows
├── 📄 BEFORE_GITHUB.md                 🔒 Seguridad antes de GitHub
├── 📄 README.md                        📚 Descripción proyecto
│
Import_Azure/
│
├── 📄 Documentación Específica
│   ├── INSTRUCTIONS.md                  🧠 Megaprompt para IA
│   ├── README_ANALYZER.md               🔍 Analizador Azure
│   └── README_DIAGRAM_GENERATOR.md      🎨 Generador de diagramas
│
├── 🔧 Scripts de Exportación
│   ├── azure_export.py                  📤 Exportar 1 suscripción
│   ├── run_exports.py                   📤 Exportar múltiples (automatizado)
│   └── examples.py                      📖 Ejemplos de ejemplos
│
├── 📊 Scripts de Análisis
│   ├── azure_infrastructure_analyzer.py 🔍 Analizar infraestructura JSON
│   ├── requirements_analyzer.txt        📦 Dependencias para análisis
│   └── INSTRUCTIONS.md                  📖 Instrucciones detalladas
│
├── 🎨 Scripts de Generación de Diagramas
│   ├── generate_network_flow_diagram.py           ✏️ Básico
│   ├── generate_network_flow_diagram_enhanced.py  ✨ Con NSGs (RECOMENDADO)
│   ├── requirements_diagram_generator.txt         📦 Dependencias
│   └── INSTRUCTIONS.md                           📖 Instrucciones detalladas
│
├── 🐳 Scripts de Automatización (Docker)
│   ├── run_diagram_in_docker.py                  ⚙️ Generar múltiples (básico)
│   ├── run_diagram_enhanced_in_docker.py         ⚙️ Múltiples enhanced (RECOMENDADO)
│   └── Dockerfile (generado en runtime)          🐳
│
├── 📦 Dependencias
│   ├── requirements.txt                 📋 Todas las dependencias
│   ├── requirements_analyzer.txt        📋 Solo análisis
│   └── requirements_diagram_generator.txt 📋 Solo diagramas
│
├── 📁 Carpetas de Trabajo
│   ├── exports/                         📁 Archivos JSON exportados
│   │   ├── *.json                       (creados por azure_export.py)
│   │   └── (vacía al inicio)
│   ├── diagrams/                        📁 Diagramas generados
│   │   ├── *.png                        (vista estática)
│   │   ├── *.dot                        (código GraphViz)
│   │   ├── *.drawio                     (editable)
│   │   └── (vacía al inicio)
│   └── reports/                         📁 Reportes de análisis
│       ├── infrastructure_summary.txt   (creado por analizador)
│       ├── sql_resources.json
│       ├── storage_accounts.json
│       └── virtual_machines.json
│
└── 🌍 Archivos de Datos (Ejemplos)
    ├── azure-infraestructure.json       📊 Ejemplo de JSON exportado
    └── example_infrastructure.json      📊 Ejemplo adicional
```

---

## 📄 Descripción Detallada de Archivos

### Documentación

#### `INDICE_DOCUMENTACION.md` ⭐ EMPIEZA AQUÍ
- **Propósito**: Índice maestro y navegación
- **Audiencia**: Todos los usuarios
- **Contenido**: Guía de qué documento leer según tus necesidades
- **Tiempo de lectura**: 2 minutos

#### `GUIA_RAPIDA.md` ⚡
- **Propósito**: Referencia rápida
- **Audiencia**: Usuarios con prisa
- **Contenido**: Comandos esenciales, flujo de 3 pasos, troubleshooting
- **Tiempo de lectura**: 5 minutos

#### `GUIA_COMPLETA.md` 📖
- **Propósito**: Documentación exhaustiva
- **Audiencia**: Usuarios que quieren entender todo
- **Contenido**: Visión general, instalación, pasos detallados, ejemplos, troubleshooting
- **Tiempo de lectura**: 30 minutos

#### `MATRIZ_REQUISITOS.md` ✅
- **Propósito**: Validación de requisitos y checklist
- **Audiencia**: Usuarios que necesitan verificar su setup
- **Contenido**: Checklist de instalación, tabla de errores, verificación
- **Tiempo de lectura**: 10 minutos

#### `INSTRUCTIONS.md` 🧠
- **Propósito**: Megaprompt para personalización con IA
- **Audiencia**: Usuarios avanzados que quieren scripts personalizados
- **Contenido**: Instrucciones detalladas para generar scripts con IA
- **Tiempo de lectura**: 15 minutos

### Scripts de Exportación

#### `azure_export.py` 📤 - Exportar Suscripción
```bash
python azure_export.py -s "subscription-id" -o output.json
```
- **Función**: Exporta infraestructura de 1 suscripción Azure
- **Requisitos**: Azure CLI login, ID de suscripción válido
- **Salida**: `exports/output.json`
- **Tiempo típico**: 2-10 minutos (depende del tamaño)
- **Uso**: Exportación inicial o de suscripción individual

#### `run_exports.py` 📤 - Exportar Múltiples (Automatizado)
```bash
python run_exports.py
```
- **Función**: Exporta TODAS las suscripciones definidas automáticamente
- **Requisitos**: Editar el archivo antes con tus subscription IDs
- **Salida**: Múltiples archivos en `exports/`
- **Tiempo típico**: 10-60 minutos (depende de cantidad y tamaño)
- **Uso**: Automatizar exportación de múltiples suscripciones
- **Nota**: Edita la lista `subscriptions` antes de ejecutar

#### `examples.py` 📖
- **Función**: 10 ejemplos prácticos de cómo usar el analizador
- **Requisitos**: JSON exportado
- **Salida**: Reportes en consola y carpeta `reports/`
- **Uso**: Aprender las capacidades del analizador

### Scripts de Análisis

#### `azure_infrastructure_analyzer.py` 🔍
- **Función**: Analiza y extrae información de JSON exportado
- **Requisitos**: Python 3.6+ (solo estándar library)
- **Salida**: 
  - Resumen en consola
  - Archivos JSON con detalles por tipo de recurso
  - Archivos de texto con reportes
- **Uso**: Entender tu infraestructura en detalle
- **Características**:
  - Extrae SQL resources, storage, VMs, etc.
  - Genera reportes organizados
  - Exporta para integración con otras herramientas

#### `requirements_analyzer.txt` 📦
- **Contenido**: Dependencias para análisis (vacío - solo usa standard library)
- **Uso**: Documentación de que NO hay dependencias adicionales

### Scripts de Generación de Diagramas

#### `generate_network_flow_diagram.py` ✏️ - Básico
```bash
python generate_network_flow_diagram.py input.json -o diagrama
```
- **Función**: Genera diagrama básico de topología de red
- **Requisitos**: GraphViz, paquetes Python
- **Salida**: 3 archivos en `diagrams/`
  - `.png` (imagen estática)
  - `.dot` (código GraphViz)
  - `.drawio` (editable)
- **Características**:
  - Topología Hub-Spoke
  - VNets y subnets
  - VMs, Load Balancers, SQL
  - Peerings de red
- **Tiempo**: 30-120 segundos (depende del tamaño)

#### `generate_network_flow_diagram_enhanced.py` ✨ - Enhanced (RECOMENDADO)
```bash
python generate_network_flow_diagram_enhanced.py input.json -o diagrama
```
- **Función**: Genera diagrama con características adicionales
- **Requisitos**: GraphViz, paquetes Python
- **Salida**: Mismos 3 formatos que versión básica
- **Características adicionales**:
  - ✨ Network Security Groups (NSGs) visualizados
  - ✨ IPs privadas de VMs mostradas
  - ✨ Mejor visualización de Private Endpoints
  - ✨ Resumen de reglas de seguridad
  - ✨ Colores diferenciados por tipo
- **Diferencia principal**: Incluye información de seguridad (NSGs)
- **Recomendación**: Usa esta versión por defecto

#### `requirements_diagram_generator.txt` 📦
```
diagrams>=0.23.1
graphviz>=0.20
```
- **Contenido**: Dependencias mínimas para generar diagramas
- **Uso**: Instalación selectiva si solo quieres diagramas

### Scripts de Automatización (Docker)

#### `run_diagram_in_docker.py` ⚙️
```bash
python run_diagram_in_docker.py
```
- **Función**: Procesa TODOS los JSON en `exports/` con Docker
- **Requisitos**: Docker instalado y corriendo
- **Salida**: Múltiples diagramas en `diagrams/`
- **Ventajas**:
  - No necesita instalar GraphViz localmente
  - ✅ **Soluciona problema de graphviz2drawio en Windows**
  - Aislamiento de dependencias
  - Mejor para CI/CD
  - Procesa múltiples exportaciones automáticamente
- **Versión**: Usa diagrama básico
- **Tiempo**: 1-5 minutos (más rápido que local)
- **⚠️ Para Windows**: RECOMENDADO - evita problemas de compilación

#### `run_diagram_enhanced_in_docker.py` ⚙️ - RECOMENDADO
```bash
python run_diagram_enhanced_in_docker.py
```
- **Función**: Procesa JSON con Docker usando versión ENHANCED (con NSGs)
- **Requisitos**: Docker
- **Salida**: Múltiples diagramas con NSGs en `diagrams/`
- **Diferencia**: Usa `generate_network_flow_diagram_enhanced.py`
- **Recomendación**: Usa esta por defecto (mejor que versión básica)
- **Mejor para**: Infraestructuras grandes con múltiples suscripciones
- **Soporte Windows**: ✅ Proporciona entorno Linux donde graphviz2drawio funciona perfectamente
- **Ventaja extra**: Procesa todos los JSONs automáticamente en un paso

### Dependencias

#### `requirements.txt` 📋 - Todas
```
# Core Azure packages
azure-identity
azure-core
# ... (45+ paquetes)
```
- **Contenido**: TODAS las dependencias necesarias
- **Uso**: `pip install -r requirements.txt`
- **Tamaño instalado**: ~200 MB
- **Recomendación**: Instala esto si:
  - Quieres usar TODAS las características
  - Harás exportación Y diagramas
  - Quieres máxima compatibilidad

#### `requirements_analyzer.txt` 📋 - Solo Análisis
- **Contenido**: Vacío (solo Python estándar)
- **Uso**: Si solo quieres analizar, no hay que instalar nada
- **Tamaño instalado**: 0 MB

#### `requirements_diagram_generator.txt` 📋 - Solo Diagramas
```
diagrams>=0.23.1
graphviz>=0.20
```
- **Uso**: `pip install -r requirements_diagram_generator.txt`
- **Tamaño**: ~50 MB
- **Recomendación**: Instala esto si solo quieres generar diagramas

### Archivos de Datos (Ejemplos)

#### `azure-infraestructure.json` 📊
- **Tipo**: Ejemplo de JSON exportado
- **Uso**: Referencia de estructura, pruebas
- **Tamaño**: 2-5 MB
- **Contiene**: Muestra de infraestructura real

---

## 🎯 Flujos de Uso Comunes

### Flujo 1: Exportar + Diagrama Simple (15 min)
```bash
# 1. Exportar
python azure_export.py -s "sub-id" -o infra.json

# 2. Generar diagrama
python generate_network_flow_diagram_enhanced.py infra.json

# 3. Ver resultado
# Abre diagrams/diagram_1.png
```

**Archivos usados:**
- `azure_export.py`
- `generate_network_flow_diagram_enhanced.py`
- `requirements.txt`

### Flujo 2: Automatización Completa (1h)
```bash
# 1. Configurar suscripciones en run_exports.py
# 2. Ejecutar
python run_exports.py

# 3. Generar todos los diagramas
python run_diagram_enhanced_in_docker.py

# 4. Revisar
# Abre diagrams/ para ver todos los resultados
```

**Archivos usados:**
- `run_exports.py`
- `run_diagram_enhanced_in_docker.py`
- `requirements.txt`
- Docker

### Flujo 3: Análisis de Infraestructura
```bash
# 1. Exportar (si no tienes JSON)
python azure_export.py -s "sub-id" -o data.json

# 2. Analizar
python azure_infrastructure_analyzer.py

# 3. Ver reportes
# Abre reports/ para detalles
```

**Archivos usados:**
- `azure_export.py`
- `azure_infrastructure_analyzer.py`
- No requiere dependencias adicionales

### Flujo 4: Personalización con IA
```bash
# 1. Leer megaprompt
cat INSTRUCTIONS.md

# 2. Copiar a Claude/ChatGPT
# [Proporcionar INSTRUCTIONS.md + JSON ejemplo]

# 3. Recibir script personalizado
# [Integrar en proyecto]

# 4. Ejecutar
python tu_script_personalizado.py
```

**Archivos usados:**
- `INSTRUCTIONS.md`
- Templates de JSON

---

## 📊 Matriz de Qué Script Usar

| Necesidad | Script | Requisitos | Salida |
|-----------|--------|-----------|--------|
| Exportar 1 suscripción | `azure_export.py` | Azure CLI | 1 JSON |
| Exportar múltiples | `run_exports.py` | Azure CLI, editar archivo | N JSONs |
| Analizar JSON | `azure_infrastructure_analyzer.py` | Solo Python | Reportes |
| Diagrama simple | `generate_network_flow_diagram.py` | GraphViz | 3 formatos |
| Diagrama con NSGs | `generate_network_flow_diagram_enhanced.py` | GraphViz | 3 formatos |
| Múltiples diagramas | `run_diagram_in_docker.py` | Docker | N diagramas |
| Múltiples + NSGs | `run_diagram_enhanced_in_docker.py` | Docker | N diagramas |

---

## 🔍 Árboles de Decisión

### "¿Qué script ejecuto?"

```
¿Tengo JSON exportado?
├─ NO → python azure_export.py -s "ID" -o output.json
│       (Luego vuelve aquí)
│
└─ SÍ ─→ ¿Cuántos archivos JSON?
         ├─ 1 → ¿Quiero NSGs?
         │       ├─ SÍ → python generate_network_flow_diagram_enhanced.py archivo.json
         │       └─ NO → python generate_network_flow_diagram.py archivo.json
         │
         └─ 2+ → ¿Tengo Docker?
                 ├─ SÍ → python run_diagram_enhanced_in_docker.py
                 └─ NO → Ejecuta generate_network_flow_diagram_enhanced.py para cada uno
```

### "¿Qué documentación leo?"

```
¿Necesito empezar YA?
├─ SÍ (ahora) → GUIA_RAPIDA.md
├─ Luego → GUIA_COMPLETA.md
├─ Validar setup → MATRIZ_REQUISITOS.md
└─ Personalizar → INSTRUCTIONS.md
```

---

## 💾 Archivos Generados (No en este repo)

Estos archivos se crean al ejecutar los scripts:

```
exports/                      (creados por azure_export.py)
├── Produccion.json
├── Development.json
└── ...

diagrams/                     (creados por generate_network_flow_diagram*.py)
├── diagram_Produccion.png
├── diagram_Produccion.dot
├── diagram_Produccion.drawio
└── ...

reports/                      (creados por azure_infrastructure_analyzer.py)
├── infrastructure_summary.txt
├── sql_resources.json
├── storage_accounts.json
└── virtual_machines.json
```

---

## 🚀 Próximos Pasos

1. **Lee el índice**: [INDICE_DOCUMENTACION.md](./INDICE_DOCUMENTACION.md)
2. **Elige tu camino**:
   - Principiante: [GUIA_RAPIDA.md](./GUIA_RAPIDA.md)
   - Completo: [GUIA_COMPLETA.md](./GUIA_COMPLETA.md)
   - Verificar: [MATRIZ_REQUISITOS.md](./MATRIZ_REQUISITOS.md)
   - Personalizar: [INSTRUCTIONS.md](./INSTRUCTIONS.md)
3. **Ejecuta tus primeros comandos**
4. **Revisa tus diagramas**

---

## 📞 Resumen

| Necesidad | Archivo | Tiempo |
|-----------|---------|--------|
| Entender estructura | Este README | 5 min |
| Empezar rápido | GUIA_RAPIDA.md | 5 min |
| Documentación completa | GUIA_COMPLETA.md | 30 min |
| Verificar requisitos | MATRIZ_REQUISITOS.md | 10 min |
| Personalizar con IA | INSTRUCTIONS.md | 15 min |

---

**Versión:** 1.0.0  
**Actualizado:** Febrero 2026  
**Autor:** Azure Architecture Diagrams Team

**¡Comienza por [INDICE_DOCUMENTACION.md](./INDICE_DOCUMENTACION.md)!** 🚀
