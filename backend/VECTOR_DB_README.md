# 🧠 Base de Datos Vectorial - Gober

## 📋 Descripción

La base de datos vectorial de Gober permite al agente conversacional acceder a información específica y actualizada de todos los documentos oficiales de Santander Territorio inteligente mediante búsqueda semántica avanzada.

## ✨ Características

- **Procesamiento automático**: PDFs y archivos Excel se procesan automáticamente
- **Búsqueda semántica**: Encuentra información relevante usando lenguaje natural
- **Embeddings multilingües**: Optimizado para español con soporte multiidioma
- **Metadatos contextuales**: Cada fragmento incluye información de fuente, página, tipo, etc.
- **Integración transparente**: Se integra automáticamente con el agente conversacional

## 📁 Estructura de Archivos

```
backend/
├── vector_db.py              # Gestor principal de base de datos vectorial
├── santander_knowledge.py    # Integración con el agente conversacional
├── init_database.py          # Script de inicialización
├── agent.py                  # Agente principal (modificado)
├── data/                     # Directorio de documentos fuente
│   ├── *.pdf                # Documentos PDF
│   └── *.xlsx               # Archivos Excel
└── chroma_db/               # Base de datos vectorial (generada automáticamente)
```

## 🚀 Instalación y Configuración

### 1. Dependencias

Las dependencias ya están incluidas en `requirements.txt`:

```
chromadb
langchain
langchain-community
PyPDF2
pandas
openpyxl
sentence-transformers
numpy
scipy
```

### 2. Inicialización

#### Opción A: Inicialización Automática
El agente cargará automáticamente los documentos la primera vez que se ejecute.

#### Opción B: Inicialización Manual
```bash
# Inicialización básica
python init_database.py

# Limpiar y recargar todo
python init_database.py --clear --stats --test

# Solo mostrar estadísticas
python init_database.py --stats
```

### 3. Opciones del Script de Inicialización

| Opción | Descripción |
|--------|-------------|
| `--clear` | Limpia la base de datos antes de cargar |
| `--stats` | Muestra estadísticas detalladas |
| `--test` | Ejecuta búsquedas de prueba |
| `--data-dir` | Directorio de documentos (default: ./data) |
| `--db-dir` | Directorio de base de datos (default: ./chroma_db) |

## 📊 Documentos Soportados

### Tipos de Documentos Procesados

- **📊 Informe de Gestión**: Documentos principales del PDD
- **📄 Informe Ejecutivo**: Resúmenes ejecutivos
- **📈 Tablero de Control**: Indicadores y métricas
- **📋 Datos Complementarios**: Archivos Excel con datos específicos

### Formatos Soportados

- **PDF**: Extracción de texto por páginas con metadatos
- **Excel**: Procesamiento de múltiples hojas con estructura tabular

## 🔍 Funcionalidades de Búsqueda

### Búsqueda Básica
```python
from santander_knowledge import search_santander_documents

# Búsqueda simple
result = await search_santander_documents("Plan de Desarrollo Departamental")
```

### Búsqueda Avanzada
```python
from santander_knowledge import knowledge_manager

# Búsqueda con filtros
results = await knowledge_manager.search_documents(
    query="ejecución presupuestal",
    n_results=5,
    document_type="informe_gestion"
)
```

### Obtener Contexto
```python
from santander_knowledge import get_document_context

# Obtener contexto para el agente
context = await get_document_context("indicadores de educación")
```

## 📈 Tipos de Consultas Soportadas

### Ejemplos de Consultas Efectivas

✅ **Consultas específicas**:
- "Plan de Desarrollo Departamental avances"
- "ejecución presupuestal sector educación"
- "indicadores de salud primer trimestre"
- "obras de infraestructura vial"

✅ **Consultas temáticas**:
- "turismo en Santander"
- "seguridad ciudadana"
- "desarrollo rural"
- "innovación tecnológica"

❌ **Consultas menos efectivas**:
- "todo" (muy amplio)
- "información" (muy genérico)
- "datos" (sin contexto específico)

## 🛠️ Mantenimiento

### Actualizar Documentos

1. **Agregar nuevos documentos**:
   - Copiar archivos a la carpeta `data/`
   - Ejecutar: `python init_database.py --clear`

2. **Verificar estado**:
   ```bash
   python init_database.py --stats
   ```

3. **Realizar pruebas**:
   ```bash
   python init_database.py --test
   ```

### Estadísticas de la Base de Datos

```python
from vector_db import SantanderVectorDB

db = SantanderVectorDB()
stats = db.get_document_stats()
print(stats)
```

Ejemplo de salida:
```json
{
    "total_chunks": 676,
    "document_types": {
        "documento_general": 630,
        "informe_ejecutivo": 25,
        "tablero_control": 9,
        "datos_complementarios": 12
    },
    "unique_sources": 4,
    "sources_list": [
        "1. INFORME GESTIÓN PDD-2 TRIMESTRE 2025.pdf",
        "2. Informe Ejecutivo 30 de junio_6deagosto.pdf",
        "3. Tablero de Control  Indicadores a junio 30 Definitivo.xlsx",
        "68.xlsx"
    ]
}
```

## 🔧 Integración con el Agente

### Modificaciones Realizadas en `agent.py`

1. **Import de módulos**:
   ```python
   from santander_knowledge import search_santander_documents, get_document_context
   ```

2. **Mejora en `on_user_turn_completed`**:
   - Búsqueda automática de contexto relevante
   - Inyección de información oficial en las respuestas
   - Manejo de errores robusto

3. **Instrucciones actualizadas**:
   - Inclusión de capacidades de búsqueda vectorial
   - Énfasis en respuestas con citas exactas

### Flujo de Funcionamiento

1. **Usuario hace pregunta** → 
2. **Sistema busca contexto relevante** → 
3. **Se inyecta información oficial** → 
4. **Agente responde con citas precisas**

## 🚨 Resolución de Problemas

### Problemas Comunes

**Error: "No se encontraron documentos"**
- Verificar que los archivos estén en `./data/`
- Ejecutar `python init_database.py --clear`

**Error: "Modelo de embeddings no se puede cargar"**
- Verificar conexión a internet (primera vez descarga modelo)
- Reinstalar: `pip install sentence-transformers --upgrade`

**Búsquedas no devuelven resultados relevantes**
- Usar consultas más específicas
- Verificar que los documentos contengan información relevante
- Revisar estadísticas: `python init_database.py --stats`

### Logs y Depuración

Los logs se muestran en la consola con formato:
```
2025-01-15 10:30:45 - vector_db - INFO - Procesando PDF: documento.pdf (150 páginas)
```

Para más detalles, modificar el nivel de logging en los archivos:
```python
logging.basicConfig(level=logging.DEBUG)
```

## 📝 Próximas Mejoras

- [ ] Soporte para más tipos de documentos (Word, PowerPoint)
- [ ] Interface web para administración
- [ ] Análisis de sentimientos en documentos
- [ ] Detección automática de actualizaciones
- [ ] Cache inteligente para consultas frecuentes
- [ ] Métricas de uso y rendimiento

## 📞 Soporte

Para problemas técnicos o consultas sobre la implementación, revisar:

1. Este README
2. Logs de la aplicación
3. Documentación del código fuente
4. Pruebas con `python init_database.py --test`

---

**Desarrollado para el proyecto Gober - GovLab Universidad de la Sabana**
