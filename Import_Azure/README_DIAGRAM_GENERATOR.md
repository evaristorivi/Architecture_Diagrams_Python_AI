# Azure Network Flow Diagram Generator (Enhanced)

Generar diagramas profesionales de topología de red Azure basados en la exportación JSON de infraestructura.

## Características

✅ **IPs de VMs** - Cada VM muestra su dirección IP privada (ej: `webvm-01 (10.0.1.10)`)
✅ **NSGs por Subred** - Muestra las políticas de seguridad a nivel de subred con resumen de reglas
✅ **Topología Hub-Spoke** - Detección automática de hub y spoke networks
✅ **Tráfico de Red** - Visualización de flujos de tráfico (VNet Peering, balanceadores, etc.)
✅ **Colores Profesionales** - Esquema de colores gris/blanco con iconos Azure reales
✅ **Múltiples Formatos** - PNG (vista previa), DOT (GraphViz), DrawIO (editable)

## Instalación de Dependencias

```bash
# Instalar librerías Python
pip install diagrams

# Instalar GraphViz (requerido)
# En Windows:
#   - Descargar desde: https://graphviz.org/download/
#   - O usar: choco install graphviz
# En macOS:
#   brew install graphviz
# En Linux:
#   sudo apt-get install graphviz
```

## Uso

### Uso Básico

```bash
# Generar diagrama desde JSON
python generate_network_flow_diagram_enhanced.py azure-infrastructure.json

# Con nombre personalizado
python generate_network_flow_diagram_enhanced.py azure-infrastructure.json -o mi_diagrama
```

### Archivos de Entrada

El script requiere un archivo JSON exportado desde Azure con esta estructura:

```json
{
  "subscriptions": [
    {
      "subscriptionId": "...",
      "displayName": "...",
      "resourceGroups": [
        {
          "resourceGroupName": "...",
          "resources": {
            "network": {
              "virtualNetworks": [...],
              "networkInterfaces": [...],
              "networkSecurityGroups": [...],
              "loadBalancers": [...],
              "privateEndpoints": [...]
            },
            "compute": {
              "virtualMachines": [...],
              "virtualMachineScaleSets": [...]
            },
            "sql": { "servers": [...] },
            "keyvault": { "vaults": [...] },
            "storage": { "storageAccounts": [...] }
          }
        }
      ]
    }
  ]
}
```

Puedes generar este archivo con:
```bash
python azure_export.py -s <subscription_id> -o infrastructure.json
```

## Archivos de Salida

El script genera 3 archivos en la carpeta `diagrams/`:

| Archivo | Descripción | Uso |
|---------|-------------|-----|
| `{output}.png` | Imagen PNG (vista previa estática) | Documentación, presentaciones |
| `{output}.dot` | Código GraphViz (para control de versiones) | Git, comparación de cambios |
| `{output}.drawio` | Diagrama editable (Draw.io format) | Modificar, anotar, exportar |

### Ejemplo

Si ejecutas:
```bash
python generate_network_flow_diagram_enhanced.py my_infrastructure.json
```

Generará:
```
diagrams/
  ├── network_flow_diagram.png
  ├── network_flow_diagram.dot
  └── network_flow_diagram.drawio
```

## Estructura del Diagrama

```
☁️ External
   └── Internet Users
       ↓
🏢 Hub VNet (192.168.0.0/16)
   ├─ subnet-fw (192.168.1.0/24)
   │  └─ [🔒 NSG: Allow FW Rules]
   │     └─ firewall-vm (192.168.1.4)
   └─ subnet-web (192.168.2.0/24)
      └─ [🔒 NSG: Allow HTTP, HTTPS]
         ├─ webvm-01 (192.168.2.5)
         └─ webvm-02 (192.168.2.6)
       ↓ VNet Peering
🌐 Spoke VNet (10.0.0.0/16)
   └─ subnet-app (10.0.1.0/24)
      └─ [🔒 NSG: Allow App Ports]
         └─ appvm-01 (10.0.1.10)
```

## Elementos del Diagrama

### Identificación Hub/Spoke

**Hub VNets** - Detectados si:
- Nombre contiene "hub"
- Contienen Azure Firewall o VPN Gateway
- Contienen subredes con "firewall" o "gateway" en el nombre

**Spoke VNets** - Todos los demás VNets que se conectan al hub

### Información Mostrada

#### VNets
```
🏢 VNet-Name (CIDR) [HUB]
```

#### Subnets
```
subnet-name (CIDR)
[🔒 NSG: Allow HTTP, HTTPS, SSH]
```

#### Virtual Machines
```
vm-name (private-ip)
Ejemplo: webvm-01 (10.0.1.15)
```

#### Load Balancers
```
LoadBalancer-Name (IP)
🌐 (External) para LBs públicos
```

#### Network Security Groups (NSG)
Resumen de reglas permitidas:
- "Allow HTTP, HTTPS" 
- "Allow SSH, RDP"
- "Allow Azure Services"
- Genera automáticamente basado en las reglas definidas

### Esquema de Colores

| Elemento | Color | Hex |
|----------|-------|-----|
| Hub VNet | Gris claro | #E8E8E8 |
| Spoke VNet | Muy claro | #F5F5F5 |
| Subnet (Firewall) | Gris oscuro | #E0E0E0 |
| Subnet (Web/App/Data) | Gris claro | #F0F0F0 |
| Subnet (Default) | Blanco | #FFFFFF |

### Emojis Utilizados

- ☁️ = Suscripción Azure
- 📂 = Resource Group
- 🏢 = Hub Network
- 🌐 = Spoke Network / External LB
- 🔒 = Network Security Group
- 🔥 = Firewall/NVA
- 🌍 = Internet
- 🔗 = VNet Peering / Conexión

## Opciones de Línea de Comandos

```
Uso: python generate_network_flow_diagram_enhanced.py [-h] [-o OUTPUT] input

Argumentos:
  input                 Archivo JSON de entrada (requerido)
  -o, --output OUTPUT   Prefijo del archivo de salida (default: network_flow_diagram)
  -h, --help            Mostrar esta ayuda
```

## Ejemplos

### Ejemplo 1: Diagrama simple

```bash
python generate_network_flow_diagram_enhanced.py azure-infrastructure.json
```

Genera: `diagrams/network_flow_diagram.{png,dot,drawio}`

### Ejemplo 2: Nombre personalizado

```bash
python generate_network_flow_diagram_enhanced.py my_infrastructure.json -o mi_topologia
```

Genera: `diagrams/mi_topologia.{png,dot,drawio}`

### Ejemplo 3: Múltiples suscripciones

Combina todas las suscripciones del JSON en un único diagrama:

```bash
# Primero exporta todas tus suscripciones
python run_exports.py

# Luego crea un diagrama consolidado (requiere agregar lógica de merge en el JSON)
python generate_network_flow_diagram_enhanced.py all_subscriptions_combined.json
```

## Edición del Diagrama en Draw.io

1. Abre el archivo `.drawio` generado
2. En https://app.diagrams.net o en Draw.io desktop
3. Puedes:
   - ✏️ Reposicionar elementos
   - ✏️ Cambiar colores
   - ✏️ Agregar anotaciones
   - ✏️ Ajustar conexiones
   - ✏️ Exportar a otros formatos (PDF, SVG, etc.)

## Solución de Problemas

### Error: "No module named 'diagrams'"

```bash
pip install diagrams
```

### Error: "Can't find dot executable"

GraphViz no está instalado o no está en PATH:
- Windows: Descargar desde graphviz.org
- macOS: `brew install graphviz`
- Linux: `sudo apt install graphviz`

### Error: "File not found"

Verifica que el archivo JSON existe y que la ruta es correcta:
```bash
# Ruta relativa
python generate_network_flow_diagram_enhanced.py azure-infrastructure.json

# Ruta absoluta
python generate_network_flow_diagram_enhanced.py C:\path\to\azure-infrastructure.json
```

### NSGs no aparecen

Asegúrate que los NSGs están en el JSON exportado:
- `resources.network.networkSecurityGroups`
- Cada subred debe referenciar el NSG en `subnet.network_security_group.id`

### IPs de VMs no aparecen

Verifica que NICs están cargadas con:
- `resources.network.networkInterfaces`
- Cada NIC debe tener `ip_configurations[0].private_ip_address`

## Rendimiento

| Número de Recursos | Tiempo Aproximado | Tamaño PNG |
|--------------------|------------------|-----------|
| < 50 | < 1 segundo | < 100 KB |
| 50-200 | 1-5 segundos | 100-500 KB |
| > 200 | 5-30 segundos | > 500 KB |

Para diagramas muy grandes, considera dividir por subscription o resource group.

## Personalización

### Cambiar colores

Edita el diccionario `COLORS` en el script:

```python
COLORS = {
    'hub_vnet': '#YOUR_COLOR',
    'spoke_vnet': '#YOUR_COLOR',
    ...
}
```

### Agregar más información al diagrama

Modifica el método `_render_resource()` para incluir atributos adicionales:

```python
label = f"{resource_name}\n({ip})\n{vm_size}"
```

## Salida de Consola

```
📂 Loading azure-infrastructure.json...
✅ Infrastructure loaded
🔍 Analyzing topology...
✅ Analysis complete: 47 resources
🏢 Detected 1 Hub VNet(s), 2 Spoke VNet(s)
🎨 Generating diagram...
✅ Diagram generated: diagrams/network_flow_diagram

✅ Complete!

📊 Summary:
   Total Resources: 47
   Hub VNets: 1
   Spoke VNets: 2
   Output Directory: diagrams/
```

## Limitaciones Conocidas

- ❌ No muestra detalles de Application Gateway (placeholder)
- ❌ No muestra rutas personalizadas (se puede agregar)
- ❌ No muestra Azure Bastion (se puede agregar)
- ❌ Draw.io conversion requiere `graphviz2drawio` (degradación graciosa si no está disponible)

## Requisitos del Sistema

- Python 3.6+
- GraphViz (sistema operativo)
- 1+ GB RAM disponible

## Roadmap

- [ ] Soporte para Application Gateway
- [ ] Visualización de rutas personalizadas
- [ ] Soporte para Azure Bastion
- [ ] Estadísticas de tráfico
- [ ] Comparación de topologías (antes/después)
- [ ] Exportación a formato Visio

## Licencia

MIT

## Soporte

Para reportar issues o sugerencias, contacta a: evaristo.rivieccio@colex.grupo-sm.com
