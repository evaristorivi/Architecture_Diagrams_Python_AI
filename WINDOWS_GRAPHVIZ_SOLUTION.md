# ⚠️ Windows: Solución de Problema graphviz2drawio

## El Problema

En Windows, al intentar instalar `graphviz2drawio` ves este error:

```
ERROR: Microsoft Visual C++ 14.0 or greater is required
error: Microsoft Visual C++ 14.0 is required. Get it with "Microsoft C++ Build Tools"
ERROR: Failed building wheel for pygraphviz
```

### ¿Por qué sucede?

`graphviz2drawio` es una librería Python que **requiere compilación C/C++** para convertir archivos GraphViz a formato DrawIO.

En **Linux y macOS** esto viene preconfigurado, pero en **Windows necesitas Microsoft Visual C++ Build Tools**.

---

## 🎯 Soluciones (Ordenadas por Recomendación)

### ✅ Solución 1: USAR DOCKER (RECOMENDADA)

**¿Por qué?**
- Funciona 100% al primer intento
- Sin instalar compiladores
- Más rápido que alternativas
- Procesa múltiples JSONs automáticamente

**Cómo:**

```bash
# En plaats de:
# pip install graphviz2drawio  ❌

# Ejecuta:
python run_diagram_enhanced_in_docker.py  ✅
```

**¿Por qué funciona?**

Docker levanta un contenedor Linux dentro de Windows:
- Dentro de Linux, `graphviz2drawio` se compila correctamente
- No necesitas build tools de C++ en Windows
- Todo funciona como si estuvieras en Linux

**Ventajas:**
- ✅ Funciona en Windows 10/11
- ✅ Procesa todos los JSON en `exports/` automáticamente
- ✅ Genera PNG, DOT, DrawIO para cada uno
- ✅ Aislamiento - no afecta tu sistema
- ✅ Más rápido que instalar localmente

**Requisito único:**
```bash
# Tener Docker instalado y corriendo
docker --version
```

---

### 📥 Solución 2: Instalar Microsoft C++ Build Tools

**Si DEBES instalar localmente (y no tienes Docker):**

**Paso 1: Descargar Visual C++ Build Tools**

1. Ve a: https://visualstudio.microsoft.com/visual-cpp-build-tools/
2. Descarga "Visual Studio Community" o "Build Tools for Visual Studio"
3. Ejecuta el instalador

**Paso 2: Instalar con los componentes correctos**

Cuando te pida qué instalar:
```
☑ Desktop development with C++
  ↳ MSVC C++ x64/x86 build tools
  ↳ C++ core features
  ↳ Windows 10/11 SDK
```

**Paso 3: Reiniciar Command Prompt/PowerShell completamente**

(Cierra y abre una nueva ventana)

**Paso 4: Instalar**

```bash
# Actualiza pip, setuptools, wheel
python.exe -m pip install --upgrade pip setuptools wheel

#Instala graphviz.org
https://graphviz.org/download/
# Ahora intenta instalar graphviz2drawio
pip install pygraphviz --config-settings="--global-option=build_ext" --config-settings="--global-option=-IC:\Program Files\Graphviz\include" --config-settings="--global-option=-LC:\Program Files\Graphviz\lib"
```

**Tiempo total:** 30-45 minutos (descarga e instalación de Build Tools)

---

### 🔧 Solución 3: Omitir DrawIO (Mínimo)

**Si solo necesitas PNG y DOT (sin DrawIO):**

```bash
# Instalar solo lo necesario
pip install diagrams graphviz>=0.20.3

# NO instalar graphviz2drawio
# pip install graphviz2drawio  ❌
```

**Resultado:**
- ✅ `diagram.png` - Imagen estática (funciona)
- ✅ `diagram.dot` - Código GraphViz (funciona)
- ⚠️ `diagram.drawio` - No se generará

**Comando para generar:**
```bash
# Generará PNG y DOT, DrawIO fallará (pero no bloquea)
python generate_network_flow_diagram_enhanced.py infrastructure.json
```

Los PNG y DOT se generarán correctamente, solo faltará el .drawio.

---

## 📊 Comparativa de Soluciones

| Solución | Tiempo | Complejidad | Funciona 100% |
|----------|--------|-------------|--------------|
| **1. Docker** | 5 min | Fácil | ✅ Sí |
| **2. Build Tools** | 45 min | Media | ✅ Sí |
| **3. Sin DrawIO** | 2 min | Muy fácil | ⚠️ Parcial |

**RECOMENDACIÓN:** Docker (Solución 1)

---

## 🚀 Guía Paso a Paso con Docker

### 1. Verifica que Docker está instalado

```bash
docker --version
```

Si no está, descárgalo desde: https://www.docker.com/products/docker-desktop

### 2. Asegúrate que Docker está corriendo

En Windows:
- Abre "Docker Desktop" desde el menú Inicio
- Espera a que diga "Docker Desktop is running"

O en PowerShell:
```bash
docker ps
```

Debe devolver algo (aunque sea lista vacía).

### 3. Coloca tus JSONs en la carpeta correcta

```
Import_Azure/
├── exports/
│   ├── Produccion.json
│   ├── Development.json
│   └── QA.json
├── run_diagram_enhanced_in_docker.py
└── ...
```

### 4. Ejecuta el script

```bash
# Desde la raíz del proyecto
cd Import_Azure
python run_diagram_enhanced_in_docker.py

# Espera 2-5 minutos...
```

### 5. Verifica los resultados

```bash
# Los diagramas estarán aquí:
dir diagrams/

# Verás:
# diagram_Produccion.png
# diagram_Produccion.dot
# diagram_Produccion.drawio
# ... (uno para cada JSON)
```

---

## 🔍 Troubleshooting con Docker

### Error: "Docker daemon is not running"

**Solución:**
1. Abre Docker Desktop desde Inicio
2. Espera a que diga "Docker is running"
3. Vuelve a ejecutar el comando

### Error: "docker: command not found"

**Solución:**
1. Reinicia PowerShell/CMD completamente
2. Verifica: `docker --version`

### Error: "Cannot connect to Docker daemon"

**Solución:**
```bash
# Verifica que Docker está corriendo
docker ps

# Si fallar, abre Docker Desktop y corre de nuevo
```

### Proceso muy lento

**Nota:** La primera ejecución descarga la imagen de Docker (~1GB), las posteriores son rápidas.

```bash
# Primera ejecución: 5-10 minutos
python run_diagram_enhanced_in_docker.py

# Siguientes ejecuciones: 1-2 minutos
python run_diagram_enhanced_in_docker.py
```

---

## ✅ Verificación Final

Después de ejecutar con Docker, deberías tener:

```bash
ls diagrams/
# Debería mostrar:
# - diagram_1.png
# - diagram_1.dot
# - diagram_1.drawio
# (3 archivos por cada JSON procesado)
```

Y los archivos de imagen deberían abrirse correctamente:
```bash
# En Windows, abre la imagen
start diagrams/diagram_1.png
```

---

## 🎓 ¿Cuándo NECESITAS Build Tools?

Solo si:
- ❌ No tienes Docker instalado
- ❌ Docker Desktop no funciona en tu PC
- ❌ Tu equipo no es Windows 10/11

En ese caso, sigue "Solución 2" arriba.

---

## 📌 Resumen

| Acción | Comando |
|--------|---------|
| Verificar Docker | `docker --version` |
| Ejecutar con Docker (RECOMENDADO) | `python run_diagram_enhanced_in_docker.py` |
| Ejecutar sin DrawIO | `python generate_network_flow_diagram_enhanced.py file.json` |
| Instalar Build Tools | Descargar desde Visual Studio official |

---

## 💡 Por qué Docker es la mejor opción

```
┌─────────────────────────────────────────────┐
│  DOCKER: Entorno Linux en Windows           │
├─────────────────────────────────────────────┤
│                                             │
│  Windows (tu PC)                           │
│    ↓                                        │
│  Docker Desktop                            │
│    ↓                                        │
│  Contenedor Linux                          │
│    ↓                                        │
│  graphviz2drawio funciona perfecto ✅      │
│    ↓                                        │
│  PNG, DOT, DrawIO generados ✅             │
│                                             │
│  Ventaja: Sin instalar compiladores        │
│           Sin afectar Windows              │
│           Portátil a otros PCs             │
└─────────────────────────────────────────────┘
```

---

**¿Aún tienes dudas?** Lee:
- [GUIA_COMPLETA.md](./GUIA_COMPLETA.md) - Sección Troubleshooting
- [MATRIZ_REQUISITOS.md](./MATRIZ_REQUISITOS.md) - Sección Windows

---

**Última recomendación:** 
```
Usa Docker. Es la forma más limpia, rápida y definitiva.
Evita 45 minutos de instalación de Build Tools y problemas futuros.
```
