# Matriz de Requisitos y Checklist

## 📋 Verificación de Requisitos Previos

### Sistema Operativo y Python

- [ ] **OS**: Windows 10+, macOS 10.14+, o Linux (Ubuntu 18.04+)
- [ ] **Python**: 3.8 o superior
  ```bash
  python --version
  # Debe mostrar: Python 3.8.x o superior
  ```

### Autenticación Azure

- [ ] **Azure CLI**: Instalado y funcionando
  ```bash
  az version
  # Debe mostrar información de Azure CLI
  ```
- [ ] **Credenciales Azure**: Válidas y con permisos de lectura
  ```bash
  az login
  # Debe abrir navegador para login
  ```
- [ ] **Permisos**: Acceso de lectura a las suscripciones objetivo

### Sistema (GraphViz)

- [ ] **GraphViz**: Instalado en el sistema
  ```bash
  dot -V
  # Debe mostrar: dot - graphviz version x.xx.x
  ```

**Ubicaciones comunes de instalación:**
- Windows: `C:\Program Files\Graphviz\bin\dot.exe`
- macOS: `/usr/local/bin/dot`
- Linux: `/usr/bin/dot`

### Python Dependencies

- [ ] **requirements.txt**: Disponible en el proyecto
- [ ] **Paquetes instalados**: Ejecutado `pip install -r requirements.txt`
  ```bash
  pip list | grep diagrams
  # Debe mostrar: diagrams
  
  pip list | grep azure-mgmt
  # Debe mostrar múltiples paquetes azure-mgmt-*
  ```

### Docker (Opcional, para Automatización)

- [ ] **Docker Desktop**: Instalado (si se usa automatización)
  ```bash
  docker --version
  # Debe mostrar: Docker version x.xx.x
  ```
- [ ] **Docker corriendo**: El daemon debe estar activo
  ```bash
  docker ps
  # Debe listar contenedores (puede estar vacío)
  ```

---

## 📦 Matriz de Dependencias por Funcionalidad

| Funcionalidad | Python | Azure CLI | GraphViz | Docker | Requerido |
|---------------|--------|-----------|----------|--------|-----------|
| **Exportar infraestructura** | ✅ 3.8+ | ✅ | ❌ | ❌ | Sí |
| **Generar diagrama local** | ✅ 3.8+ | ❌ | ✅ | ❌ | Sí |
| **Generar diagrama en Docker** | ✅ 3.8+ | ❌ | ❌ | ✅ | No |
| **Análisis infraestructura** | ✅ 3.8+ | ❌ | ❌ | ❌ | Sí* |
| **Automatización múltiple** | ✅ 3.8+ | ✅ | ✅ | ✅ | Opcional |

\* Usa solo librerías estándar de Python

---

## 🔧 Verificación Paso a Paso

### Paso 1: Verificar Python
```bash
# Windows
python --version
python -m pip --version

# Linux/macOS
python3 --version
python3 -m pip --version
```

**Resultado esperado:**
```
Python 3.8.10
pip 21.0.1
```

### Paso 2: Verificar Azure
```bash
az version
az account list --output table
```

**Resultado esperado:**
```
Azure CLI 2.40.0
[Lista de suscripciones]
```

### Paso 3: Verificar GraphViz
```bash
# Windows
where dot
dot -V

# Linux/macOS
which dot
dot -V
```

**Resultado esperado:**
```
C:\Program Files\Graphviz\bin\dot.exe
dot - graphviz version 2.43.0
```

### Paso 4: Verificar Python Packages
```bash
cd Import_Azure
pip install -r requirements.txt --quiet
python -c "
import diagrams
import azure.identity
import azure.mgmt.network
print('✅ Todos los paquetes están instalados correctamente')
"
```

**Resultado esperado:**
```
✅ Todos los paquetes están instalados correctamente
```

### Paso 5: Verificar Docker (Opcional)
```bash
docker --version
docker run hello-world
```

**Resultado esperado:**
```
Docker version 20.10.x
Hello from Docker!
```

---

## 📊 Checklist de Instalación Completa

### Instalación Windows
```bash
# 1. GraphViz
winget install Graphviz.Graphviz
# O descargar desde https://graphviz.org/download/

# 2. Python (3.8+)
# Descargar desde https://www.python.org/downloads/
# O: winget install Python.Python.3.11

# 3. Azure CLI
winget install Microsoft.AzureCLI

# 4. Dependencias Python
cd Import_Azure
pip install -r requirements.txt

# 5. Verificar
python ..\..\scripts\verify.py
```

### Instalación macOS
```bash
# 1. Homebrew (si no está instalado)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# 2. Python, GraphViz, Azure CLI
brew install python@3.11 graphviz
pip install --upgrade pip
curl -sL https://aka.ms/InstallAzureCLIDeb | bash

# 3. Dependencias Python
cd Import_Azure
pip3 install -r requirements.txt

# 4. Verificar
python3 verify.py
```

### Instalación Linux (Ubuntu/Debian)
```bash
# 1. Actualizar sistema
sudo apt-get update
sudo apt-get upgrade -y

# 2. Instalar dependencias
sudo apt-get install -y python3.11 python3-pip graphviz graphviz-dev

# 3. Azure CLI
curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash

# 4. Dependencias Python
cd Import_Azure
pip3 install -r requirements.txt

# 5. Verificar
python3 verify.py
```

---

## ✅ Checklist Pre-Ejecución

Antes de ejecutar cualquier script:

- [ ] Python 3.8+ instalado
- [ ] `az login` ejecutado exitosamente
- [ ] GraphViz instalado y en PATH
- [ ] Estoy en la carpeta `Import_Azure`
- [ ] Entorno virtual activado (si se usa)
- [ ] `pip install -r requirements.txt` completado
- [ ] Tengo ID de suscripción Azure válido
- [ ] Tengo permisos de lectura en la suscripción

---

## ✅ Checklist Post-Ejecución

Después de ejecutar los scripts:

- [ ] `exports/` contiene archivos JSON
- [ ] `diagrams/` contiene los 3 formatos (PNG, DOT, DrawIO)
- [ ] No hay errores en la consola
- [ ] Los diagramas se ven correctamente (abrir PNG)
- [ ] DrawIO puede importar los archivos .drawio
- [ ] Archivos DOT son código GraphViz válido

---

## 🐛 Tabla de Verificación de Errores Comunes

| Error | Causa | Verificación |
|-------|-------|--------------|
| `No module named 'diagrams'` | Paquete no instalado | `pip install diagrams` |
| `GraphViz not found` | GraphViz no en PATH | `dot -V` |
| `AzureCliCredential error` | No autenticado | `az login` |
| `Subscription not found` | ID incorrecto | `az account list` |
| `Permission denied` | Sin permisos de lectura | Consultar con admin Azure |
| `Docker not found` | Docker no instalado | `docker --version` |
| `Memory error` | Infraestructura muy grande | Usar Docker con más memoria |

---

## ⚠️ PROBLEMA CONOCIDO: graphviz2drawio en Windows

### Síntomas

Al ejecutar en Windows:
```
error: Microsoft Visual C++ 14.0 or greater is required
build failed
failed building wheel for graphviz2drawio
```

### Por qué sucede

`graphviz2drawio` requiere compilación C/C++, y Windows no tiene los compiladores necesarios por defecto.

### Soluciones

**Opción A: Usar Docker (RECOMENDADO ⭐)**
```bash
# En Windows, ejecuta en lugar de instalar localmente:
python run_diagram_in_docker.py
# O versión enhanced:
python run_diagram_enhanced_in_docker.py

# Docker proporciona un entorno Linux donde funciona perfectamente
```

**Ventajas de Docker:**
- ✅ Funciona al 100% en Windows
- ✅ Procesa múltiples JSONs automáticamente
- ✅ No requiere instalar herramientas de compilación
- ✅ Más rápido que instalar localmente

**Opción B: Instalar Microsoft C++ Build Tools**
1. Descargar: [Visual C++ Build Tools](https://visualstudio.microsoft.com/visual-cpp-build-tools/)
2. Instalar con "Desktop development with C++"
3. Reiniciar Command Prompt
4. Ejecutar:
```bash
pip install --upgrade setuptools wheel
pip install graphviz2drawio
```

**Opción C: Sin DrawIO (forma mínima)**
```bash
# DrawIO es opcional. Si falla, aún funciona:
python generate_network_flow_diagram_enhanced.py infrastructure.json

# Resultado:
# ✅ diagram.png (imagen - abre directamente)
# ✅ diagram.dot (código GraphViz)  
# ⚠️ diagram.drawio (puede fallar, pero no es crítico)
```

### Recomendación para Windows

**USAR DOCKER** - Es la forma más limpia y rápida:

```bash
# Reemplaza esto:
# pip install graphviz2drawio  ❌

# Con esto:
python run_diagram_enhanced_in_docker.py  ✅
```

Docker levanta un ambiente Linux donde `graphviz2drawio` funciona perfecto, sin necesidad de instalar compiladores en tu Windows.

---

## 📝 Notas de Versiones de Python

| Versión | Compatible | Recomendación |
|---------|-----------|---------------|
| Python 3.7 | ⚠️ Parcialmente | Actualizar a 3.8+ |
| Python 3.8 | ✅ Sí | OK |
| Python 3.9 | ✅ Sí | Recomendado |
| Python 3.10 | ✅ Sí | Recomendado |
| Python 3.11 | ✅ Sí | Última estable |
| Python 3.12 | ⚠️ En pruebas | Puede haber incompatibilidades |

**Recomendación:** Python 3.10 o 3.11

---

## 📝 Requisitos.txt Verification

```bash
# Mostrar versiones instaladas
pip show diagrams graphviz2drawio azure-identity

# Verificar ALL requirements
pip check

# Forzar reinstalación si hay problemas
pip install --force-reinstall -r requirements.txt
```

---

## 🌍 Requisitos por Región Azure

No hay requisitos específicos por región. **Todos los comandos funcionan con cualquier región Azure**.

---

## 💾 Requisitos de Espacio en Disco

| Componente | Tamaño |
|-----------|--------|
| Python 3.11 | ~100 MB |
| Paquetes pip (diagrams, azure-*) | ~200 MB |
| GraphViz | ~50 MB |
| Docker (si se usa) | ~500 MB |
| Exportación Azure (pequeña <1000 recursos) | 1-5 MB |
| Exportación Azure (grande >10000 recursos) | 10-100 MB |
| Diagramas generados (3 formatos) | 2-50 MB |
| **Total mínimo** | **~350 MB** |
| **Total recomendado** | **~2 GB** |

---

## 🔐 Requisitos de Seguridad

- ✅ **Never commit** archivos JSON con infraestructura a Git (contienen IPs/configuraciones)
- ✅ **Usa** `.gitignore` para excluir `exports/` y `diagrams/`
- ✅ **Credenciales**: `az login` usa token temporal, seguro
- ✅ **Permisos mínimos**: Solo lectura, no necesita cambiar nada
- ✅ **Datos sensibles**: Los PNG/DrawIO pueden compartirse, no contienen credenciales

---

## 🎯 Próximo Paso

Una vez confirmados todos los checkmarks ✅:

```bash
cd Import_Azure
python azure_export.py -s "YOUR-SUBSCRIPTION-ID" -o infrastructure.json
```

¡Listo para empezar! 🚀
