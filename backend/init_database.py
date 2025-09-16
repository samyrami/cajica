#!/usr/bin/env python3
"""
Script de Inicialización de Base de Datos Vectorial
====================================================

Este script inicializa y carga la base de datos vectorial con todos 
los documentos disponibles en el directorio de datos.

Uso:
    python init_database.py [opciones]

Opciones:
    --clear    Limpia la base de datos antes de cargar
    --stats    Muestra estadísticas después de la carga
    --test     Ejecuta búsquedas de prueba
"""

import argparse
import asyncio
import logging
from pathlib import Path
from vector_db import SantanderVectorDB
from santander_knowledge import SantanderKnowledge

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def setup_arg_parser():
    """
    Configura el parser de argumentos de línea de comandos
    """
    parser = argparse.ArgumentParser(
        description='Inicializar base de datos vectorial de Gober',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos de uso:
    python init_database.py                  # Carga normal
    python init_database.py --clear          # Limpia y recarga
    python init_database.py --clear --test   # Limpia, recarga y prueba
    python init_database.py --stats          # Solo muestra estadísticas
        """
    )
    
    parser.add_argument(
        '--clear',
        action='store_true',
        help='Limpia la base de datos antes de cargar los documentos'
    )
    
    parser.add_argument(
        '--stats',
        action='store_true',
        help='Muestra estadísticas detalladas después de la operación'
    )
    
    parser.add_argument(
        '--test',
        action='store_true',
        help='Ejecuta búsquedas de prueba después de la carga'
    )
    
    parser.add_argument(
        '--data-dir',
        type=str,
        default='./data',
        help='Directorio donde están los documentos fuente (default: ./data)'
    )
    
    parser.add_argument(
        '--db-dir',
        type=str,
        default='./chroma_db',
        help='Directorio de la base de datos vectorial (default: ./chroma_db)'
    )
    
    return parser

async def run_test_queries(knowledge: SantanderKnowledge):
    """
    Ejecuta consultas de prueba para verificar el funcionamiento
    
    Args:
        knowledge (SantanderKnowledge): Instancia del gestor de conocimiento
    """
    test_queries = [
        "Plan de Desarrollo Departamental",
        "ejecución presupuestal",
        "indicadores de educación",
        "sector salud",
        "obras de infraestructura",
        "turismo en Santander"
    ]
    
    logger.info("🧪 Ejecutando consultas de prueba...")
    print("\n" + "="*60)
    print("🔍 PRUEBAS DE BÚSQUEDA")
    print("="*60)
    
    for i, query in enumerate(test_queries, 1):
        print(f"\n{i}. Consulta: '{query}'")
        print("-" * 40)
        
        try:
            results = await knowledge.search_documents(query, n_results=2)
            
            if results:
                for j, result in enumerate(results, 1):
                    score = result['relevance_score']
                    source = result['metadata']['source']
                    content_preview = result['content'][:150].replace('\n', ' ')
                    
                    print(f"   Resultado {j}: {score:.1%} relevancia")
                    print(f"   Fuente: {source}")
                    print(f"   Vista previa: {content_preview}...")
                    print()
            else:
                print("   ❌ No se encontraron resultados")
                
        except Exception as e:
            print(f"   ❌ Error en consulta: {e}")

def print_stats(stats):
    """
    Imprime estadísticas de manera formateada
    
    Args:
        stats (dict): Estadísticas de la base de datos
    """
    print("\n" + "="*60)
    print("📊 ESTADÍSTICAS DE LA BASE DE DATOS")
    print("="*60)
    
    if "error" in stats:
        print(f"❌ Error: {stats['error']}")
        return
    
    print(f"📄 Total de chunks almacenados: {stats.get('total_chunks', 0):,}")
    print(f"📁 Documentos únicos procesados: {stats.get('unique_sources', 0)}")
    
    print("\n🗂️  Tipos de documentos:")
    doc_types = stats.get('document_types', {})
    for doc_type, count in doc_types.items():
        emoji = "📊" if "gestion" in doc_type else "📄"
        if "ejecutivo" in doc_type:
            emoji = "📋"
        elif "tablero" in doc_type:
            emoji = "📈"
        elif "datos" in doc_type:
            emoji = "📋"
        
        print(f"   {emoji} {doc_type.replace('_', ' ').title()}: {count}")
    
    print("\n📁 Archivos procesados:")
    sources = stats.get('sources_list', [])
    for source in sources:
        print(f"   ✅ {source}")

async def main():
    """
    Función principal del script
    """
    parser = setup_arg_parser()
    args = parser.parse_args()
    
    # Verificar que el directorio de datos existe
    data_path = Path(args.data_dir)
    if not data_path.exists():
        logger.error(f"❌ Directorio de datos no encontrado: {args.data_dir}")
        return
    
    logger.info("🚀 Iniciando inicialización de base de datos vectorial...")
    logger.info(f"📂 Directorio de datos: {args.data_dir}")
    logger.info(f"🗄️  Directorio de BD: {args.db_dir}")
    
    try:
        # Inicializar componentes
        db = SantanderVectorDB(data_dir=args.data_dir, db_dir=args.db_dir)
        knowledge = SantanderKnowledge(data_dir=args.data_dir, db_dir=args.db_dir)
        
        # Mostrar estadísticas iniciales
        initial_stats = db.get_document_stats()
        print_stats(initial_stats)
        
        # Limpiar base de datos si se solicita
        if args.clear:
            logger.info("🧹 Limpiando base de datos existente...")
            success = db.clear_database()
            if success:
                logger.info("✅ Base de datos limpiada exitosamente")
            else:
                logger.error("❌ Error limpiando base de datos")
                return
        
        # Cargar documentos si la base está vacía o si se solicitó limpieza
        current_stats = db.get_document_stats()
        if current_stats.get("total_chunks", 0) == 0 or args.clear:
            logger.info("📥 Cargando documentos a la base de datos...")
            db.load_documents()
            logger.info("✅ Carga de documentos completada")
        else:
            logger.info("ℹ️  Base de datos ya contiene documentos, omitiendo carga")
        
        # Mostrar estadísticas finales
        if args.stats:
            final_stats = db.get_document_stats()
            print_stats(final_stats)
        
        # Ejecutar pruebas si se solicita
        if args.test:
            await run_test_queries(knowledge)
        
        logger.info("🎉 Inicialización completada exitosamente")
        
    except Exception as e:
        logger.error(f"❌ Error durante la inicialización: {e}", exc_info=True)
        return

if __name__ == "__main__":
    asyncio.run(main())
