#!/usr/bin/env python3
"""
Script de prueba para verificar la funcionalidad de búsqueda vectorial
"""
import asyncio
import logging
from santander_knowledge import knowledge_manager

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def test_vector_search():
    """
    Prueba la búsqueda vectorial con consultas específicas
    """
    print("🔍 Probando búsqueda vectorial...")
    
    # Estadísticas de la base
    stats = knowledge_manager.get_stats()
    print(f"\n📊 Estadísticas de la base de datos:")
    for key, value in stats.items():
        print(f"  - {key}: {value}")
    
    # Consultas de prueba
    test_queries = [
        "Secretaría de Educación indicadores",
        "educación avances metas",
        "indicadores completados educación",
        "secretaría educación 46.8%",
        "secretaría educación presupuesto",
        "ejecución presupuestal 94.8%"
    ]
    
    print(f"\n🧪 Probando {len(test_queries)} consultas:")
    
    for i, query in enumerate(test_queries, 1):
        print(f"\n--- Prueba {i}: '{query}' ---")
        try:
            # Buscar contexto
            context = await knowledge_manager.get_context_for_query(query)
            
            if context.strip():
                print(f"✅ Encontró contexto ({len(context)} caracteres):")
                # Mostrar primeras líneas del contexto
                lines = context.split('\n')[:5]
                for line in lines:
                    if line.strip():
                        print(f"    {line[:100]}...")
                if len(lines) > 5:
                    print("    ...")
            else:
                print("❌ No encontró contexto")
                
            # Buscar con respuesta completa
            response = await knowledge_manager.answer_with_sources(query)
            print(f"📝 Fuentes encontradas: {response['found_sources']}")
            
        except Exception as e:
            print(f"❌ Error en consulta: {e}")
            logger.exception("Error en consulta")
    
    print(f"\n✅ Prueba completada")

if __name__ == "__main__":
    asyncio.run(test_vector_search())
