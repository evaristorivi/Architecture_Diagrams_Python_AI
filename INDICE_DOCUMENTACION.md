# 📚 Índice Maestro de Documentación

## Bienvenido a Azure Architecture Diagrams Generator

Este proyecto permite exportar tu infraestructura Azure e **generar diagramas profesionales de topología de red automáticamente**.

---

## 🎯 ¿Qué Documento Debo Leer?

### Si eres **Nuevo en el Proyecto**
👉 **Lee:** [GUIA_RAPIDA.md](./GUIA_RAPIDA.md)  
⏱️ **Tiempo**: 5 minutos  
📖 Contiene: Comandos básicos, flujo de 5 pasos, troubleshooting rápido

### Si necesitas **Documentación Completa**
👉 **Lee:** [GUIA_COMPLETA.md](./GUIA_COMPLETA.md)  
⏱️ **Tiempo**: 20-30 minutos  
📖 Contiene: Todo explicado en detalle, ejemplos, mejores prácticas

### Si debes **Verificar Requisitos**
👉 **Lee:** [MATRIZ_REQUISITOS.md](./MATRIZ_REQUISITOS.md)  
⏱️ **Tiempo**: 10 minutos  
📖 Contiene: Checklist de instalación, verificación, tabla de errores

### Si quieres **Personalizar con IA**
👉 **Lee:** [INSTRUCTIONS.md](Import_Azure/INSTRUCTIONS.md)  
⏱️ **Tiempo**: 15 minutos (lectura) + tiempo de IA  
📖 Contiene: Megaprompt para generar scripts personalizados con Claude/ChatGPT

### Si algo **No Funciona**
👉 **Ve a:** [MATRIZ_REQUISITOS.md](./MATRIZ_REQUISITOS.md) → Tabla de Errores  
👉 **O:** [GUIA_COMPLETA.md](./GUIA_COMPLETA.md) → Sección Troubleshooting

---

## 📊 Comparativa de Documentos

| Documento | Tipo | Nivel | Duración | Mejor Para |
|-----------|------|-------|----------|-----------|
| **GUIA_RAPIDA.md** | Referencia | Principiante | 5 min | Empezar rápido |
| **GUIA_COMPLETA.md** | Tutorial | Intermedio | 30 min | Aprender todo |
| **MATRIZ_REQUISITOS.md** | Checklist | Principiante | 10 min | Validar setup |
| **INSTRUCTIONS.md** | Megaprompt | Avanzado | 15 min | Personalización IA |
| **Este archivo** | Índice | Todos | 2 min | Orientarse |

---

## 🚀 Flujo Recomendado

### Opción A: Empezar Inmediatamente (15 min)
1. Lee [GUIA_RAPIDA.md](./GUIA_RAPIDA.md) (5 min)
2. Verifica requisitos en [MATRIZ_REQUISITOS.md](./MATRIZ_REQUISITOS.md) (3 min)
3. Ejecuta los comandos de GUIA_RAPIDA.md (7 min)
4. ✅ ¡Tienes tus primeros diagramas!

### Opción B: Aprender Completamente (45 min)
1. Lee [GUIA_COMPLETA.md](./GUIA_COMPLETA.md) completa (30 min)
2. Verifica checklist en [MATRIZ_REQUISITOS.md](./MATRIZ_REQUISITOS.md) (5 min)
3. Ejecuta ejemplos paso a paso (10 min)
4. ✅ Entiendes completamente cómo funciona

### Opción C: Personalizar for Tus Necesidades (1h)
1. Lee [GUIA_RAPIDA.md](./GUIA_RAPIDA.md) (5 min)
2. Ejecuta los comandos básicos (10 min)
3. Lee [INSTRUCTIONS.md](Import_Azure/INSTRUCTIONS.md) (15 min)
4. Copia el prompt a Claude/ChatGPT con tu requisito (5 min)
5. Integra el script generado (20 min)
6. ✅ Tienes diagramas personalizados

---

## 📋 Tabla de Contenidos por Documento

### GUIA_RAPIDA.md
- ⚡ TL;DR - Los esenciales
- 📦 Requisitos mínimos
- 🎯 Flujo principal (3 pasos)
- 🚀 Automatización
- 🤖 Uso con IA
- 📊 Archivos de salida
- ⚠️ Solución rápida de problemas
- 💡 Comandos clave
- 🔗 Recursos

### GUIA_COMPLETA.md
- 📋 Índice de contenidos
- 📊 Visión general
- 📦 Requisitos previos
- 🔧 Instalación de dependencias
- 🔄 Flujo completo del proyecto
- 👉 Pasos detallados
- 🤖 Automatización
- 🧠 Uso avanzado con prompts IA
- 📁 Archivos de salida
- 🐛 Troubleshooting
- 📝 Resumen de comandos
- 🎉 Próximos pasos

### MATRIZ_REQUISITOS.md
- 📋 Verificación de requisitos previos
- 📦 Matriz de dependencias
- 🔧 Verificación paso a paso
- 📊 Checklist de instalación (Windows, macOS, Linux)
- ✅ Checklist pre-ejecución
- ✅ Checklist post-ejecución
- 🐛 Tabla de errores comunes
- 🎓 Tabla de recursos
- 📝 Notas de versiones de Python
- 💾 Requisitos de espacio en disco
- 🔐 Requisitos de seguridad

### INSTRUCTIONS.md
- 📋 Instrucciones para IA
- 🔧 Arquitectura de solución recomendada
- 📊 Estructura JSON
- 🎯 Patrones de procesamiento
- 🧠 Lógica de diagramas
- 📁 Organización de código

---

## 🎓 Por Tipo de Usuario

### Para DevOps Engineers
1. Lee: [GUIA_COMPLETA.md](./GUIA_COMPLETA.md) - Sección "Automatización"
2. Configura: [run_diagram_enhanced_in_docker.py](./run_diagram_enhanced_in_docker.py)
3. Integra: En tu CI/CD pipeline

### Para Cloud Architects
1. Lee: [GUIA_COMPLETA.md](./GUIA_COMPLETA.md) completa
2. Personaliza: Usando [INSTRUCTIONS.md](Import_Azure/INSTRUCTIONS.md) con IA
3. Crea: Diagramas que muestren lo que necesites

### Para Administradores Azure
1. Lee: [GUIA_RAPIDA.md](./GUIA_RAPIDA.md)
2. Verifica: [MATRIZ_REQUISITOS.md](./MATRIZ_REQUISITOS.md)
3. Ejecuta: `azure_export.py` y `generate_network_flow_diagram_enhanced.py`

### Para Desarrolladores
1. Lee: [INSTRUCTIONS.md](Import_Azure/INSTRUCTIONS.md)
2. Personaliza: Crea tus propios generadores con el megaprompt
3. Contribuye: Mejora los scripts existentes

---

## 💡 Casos de Uso Comunes

### "Necesito documentar mi infraestructura Azure"
→ [GUIA_RAPIDA.md](./GUIA_RAPIDA.md) + ejecuta 3 comandos

### "Quiero automatizar esto en CI/CD"
→ [GUIA_COMPLETA.md](./GUIA_COMPLETA.md) "Automatización" + [run_diagram_enhanced_in_docker.py](./run_diagram_enhanced_in_docker.py)

### "Necesito diagramas que muestren costos"
→ [INSTRUCTIONS.md](Import_Azure/INSTRUCTIONS.md) + prompt IA personalizado

### "Tenemos 50 suscripciones"
→ [run_exports.py](./run_exports.py) + [run_diagram_enhanced_in_docker.py](./run_diagram_enhanced_in_docker.py)

### "Mi infraestructura es muy grande"
→ Exporta por suscripción + genera diagramas separados

### "Algo no funciona"
→ [MATRIZ_REQUISITOS.md](./MATRIZ_REQUISITOS.md) "Tabla de Errores"

---

## ✅ Checklist de Lectura Recomendada

Marca mientras avanzas:

- [ ] Leí la introducción de este archivo (estás aquí)
- [ ] Leí [GUIA_RAPIDA.md](./GUIA_RAPIDA.md)
- [ ] Verifiqué requisitos en [MATRIZ_REQUISITOS.md](./MATRIZ_REQUISITOS.md)
- [ ] Ejecuté mis primeros comandos
- [ ] Generé mi primer diagrama
- [ ] Leí [GUIA_COMPLETA.md](./GUIA_COMPLETA.md) (si necesito más)
- [ ] Leí [INSTRUCTIONS.md](Import_Azure/INSTRUCTIONS.md) (si quiero personalizar)
- [ ] Personalicé mi propio script (si lo necesitaba)

---

## 🔗 Índice de Comandos Rápidos

Para no tener que buscar, aquí están los comandos principales:

```bash
# Autenticación
az login

# Instalar dependencias
pip install -r requirements.txt

# Exportar Azure (1 suscripción)
python azure_export.py -s "SUBSCRIPTION-ID" -o infrastructure.json

# Exportar Azure (múltiples, automatizado)
python run_exports.py

# Generar diagrama (básico)
python generate_network_flow_diagram.py infrastructure.json

# Generar diagrama (con NSGs, recomendado)
python generate_network_flow_diagram_enhanced.py infrastructure.json -o mi_diagrama

# Generar múltiples diagramas (Docker)
python run_diagram_enhanced_in_docker.py

# Analizar infraestructura
python azure_infrastructure_analyzer.py
```

---

## 🎯 Resumen de Decisiones

**¿Solo quiero empezar?**
→ [GUIA_RAPIDA.md](./GUIA_RAPIDA.md)

**¿Necesito documentación completa?**
→ [GUIA_COMPLETA.md](./GUIA_COMPLETA.md)

**¿Necesito verificar mi setup?**
→ [MATRIZ_REQUISITOS.md](./MATRIZ_REQUISITOS.md)

**¿Quiero crear scripts personalizados?**
→ [INSTRUCTIONS.md](Import_Azure/INSTRUCTIONS.md)

**¿Necesito ejemplos específicos?**
→ Busca en la sección "Ejemplos" de GUIA_COMPLETA.md

**¿Algo no funciona?**
→ [MATRIZ_REQUISITOS.md](./MATRIZ_REQUISITOS.md) → "Troubleshooting"

---

## 📞 Navegación

| Si necesitas... | Ve a... |
|-----------------|---------|
| Empezar rápido | [GUIA_RAPIDA.md](./GUIA_RAPIDA.md) |
| Todo explicado | [GUIA_COMPLETA.md](./GUIA_COMPLETA.md) |
| Verificar requisitos | [MATRIZ_REQUISITOS.md](./MATRIZ_REQUISITOS.md) |
| Personalizar con IA | [INSTRUCTIONS.md](Import_Azure/INSTRUCTIONS.md) |
| Ver este índice | Estás aquí 👈 |

---

## 🚀 ¡Empecemos!

**Opción 1 - Rápido (5 min):**
```bash
cd Import_Azure
cat GUIA_RAPIDA.md
```

**Opción 2 - Completo (30 min):**
```bash
cd Import_Azure
cat GUIA_COMPLETA.md
```

**Opción 3 - Validar setup (10 min):**
```bash
cd Import_Azure
cat MATRIZ_REQUISITOS.md
```

---

## 📝 Notas Finales

- **Todos los archivos están en `Import_Azure/`**
- **Los comandos deben ejecutarse desde la carpeta `Import_Azure/`**
- **Archivos de salida se generan en `diagrams/` y `exports/`**
- **No necesitas todos los documentos - elige según tu necesidad**
- **Los enlaces son relativos - funcionan desde la carpeta del proyecto**

---

**Última actualización:** Febrero 2026  
**Versión:** 1.0.0  

**¿Listo? ¡Comienza por [GUIA_RAPIDA.md](./GUIA_RAPIDA.md)!** 🚀
