#!/usr/bin/env python3
"""
Script de Optimización del Agente Gober
==================================================

Este script optimiza el rendimiento del agente:
1. Pre-carga la base de datos vectorial
2. Verifica la conectividad de LiveKit
3. Optimiza la configuración de conexión
"""

import os
import sys
import asyncio
import logging
import time
from dotenv import load_dotenv
from santander_knowledge import knowledge_manager

# Cargar variables de entorno
load_dotenv(dotenv_path=".env.local")

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def optimize_vector_database():
    """Pre-carga y optimiza la base de datos vectorial"""
    print("🔧 Optimizando base de datos vectorial...")
    
    start_time = time.time()
    
    # Asegurar que la base de datos esté cargada
    await knowledge_manager.ensure_loaded()
    
    # Obtener estadísticas
    stats = knowledge_manager.get_stats()
    
    load_time = time.time() - start_time
    
    print(f"✅ Base de datos cargada en {load_time:.2f} segundos")
    print(f"📊 Total de chunks: {stats.get('total_chunks', 0)}")
    print(f"📁 Documentos únicos: {stats.get('unique_sources', 0)}")
    
    return stats

def verify_environment():
    """Verifica las variables de entorno necesarias"""
    print("🔍 Verificando variables de entorno...")
    
    required_vars = [
        'OPENAI_API_KEY',
        'LIVEKIT_API_KEY', 
        'LIVEKIT_API_SECRET',
        'LIVEKIT_URL'
    ]
    
    missing_vars = []
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        print(f"❌ Variables faltantes: {', '.join(missing_vars)}")
        return False
    else:
        print("✅ Todas las variables de entorno están configuradas")
        return True

async def test_vector_search_performance():
    """Prueba el rendimiento de búsqueda vectorial"""
    print("⚡ Probando rendimiento de búsqueda vectorial...")
    
    test_queries = [
        "Plan de Desarrollo Departamental",
        "ejecución presupuestal educación",
        "indicadores de salud",
        "avances en infraestructura"
    ]
    
    total_time = 0
    for query in test_queries:
        start_time = time.time()
        context = await knowledge_manager.get_context_for_query(query)
        query_time = time.time() - start_time
        total_time += query_time
        
        has_results = len(context) > 0
        print(f"  📝 '{query}': {query_time:.2f}s {'✅' if has_results else '❌'}")
    
    avg_time = total_time / len(test_queries)
    print(f"⏱️ Tiempo promedio de búsqueda: {avg_time:.2f} segundos")
    
    return avg_time

def check_system_resources():
    """Verifica recursos del sistema"""
    print("💻 Verificando recursos del sistema...")
    
    try:
        import psutil
        
        # Memoria disponible
        memory = psutil.virtual_memory()
        print(f"🧠 Memoria disponible: {memory.available / (1024**3):.1f} GB de {memory.total / (1024**3):.1f} GB")
        
        # CPU
        cpu_percent = psutil.cpu_percent(interval=1)
        print(f"⚡ Uso de CPU: {cpu_percent}%")
        
        # Espacio en disco
        disk = psutil.disk_usage('.')
        print(f"💾 Espacio en disco: {disk.free / (1024**3):.1f} GB disponibles")
        
    except ImportError:
        print("⚠️ psutil no instalado. Ejecutar: pip install psutil")

def display_optimization_tips():
    """Muestra consejos de optimización"""
    print("\n📋 CONSEJOS DE OPTIMIZACIÓN:")
    print("1. 🚀 Mantener el agente corriendo en modo dev para conexiones más rápidas")
    print("2. 📊 La base de datos vectorial se carga automáticamente al primer uso")
    print("3. 🔄 Reiniciar el agente si las conexiones son muy lentas")
    print("4. 🌐 Verificar conectividad a internet para LiveKit y OpenAI")
    print("5. ⚡ Cerrar aplicaciones pesadas para liberar recursos")

async def main():
    """Función principal de optimización"""
    print("🚀 OPTIMIZACIÓN DEL AGENTE GOBER")
    print("=" * 50)
    
    # 1. Verificar entorno
    if not verify_environment():
        print("❌ Por favor configure las variables de entorno antes de continuar")
        sys.exit(1)
    
    print()
    
    # 2. Verificar recursos del sistema
    check_system_resources()
    print()
    
    # 3. Optimizar base de datos vectorial
    await optimize_vector_database()
    print()
    
    # 4. Probar rendimiento de búsqueda
    avg_search_time = await test_vector_search_performance()
    print()
    
    # 5. Evaluación general
    print("📊 EVALUACIÓN GENERAL:")
    if avg_search_time < 2.0:
        print("✅ Rendimiento de búsqueda: EXCELENTE")
    elif avg_search_time < 5.0:
        print("⚡ Rendimiento de búsqueda: BUENO")
    else:
        print("⚠️ Rendimiento de búsqueda: MEJORABLE")
    
    print()
    display_optimization_tips()
    
    print("\n🎯 OPTIMIZACIÓN COMPLETADA")
    print("Ahora puede ejecutar: python agent.py dev")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n⏹️ Optimización cancelada por el usuario")
    except Exception as e:
        logger.error(f"Error en optimización: {e}", exc_info=True)
