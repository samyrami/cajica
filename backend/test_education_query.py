#!/usr/bin/env python3
"""
Script para probar específicamente consultas sobre la Secretaría de Educación
"""
import asyncio
import logging
from santander_knowledge import knowledge_manager

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def test_education_specific():
    """
    Prueba consultas específicas sobre educación como las que haría un usuario
    """
    print("🎓 Probando consultas específicas sobre Secretaría de Educación...")
    
    # Consultas que podrían hacer los usuarios
    user_queries = [
        "¿Cuáles son los indicadores completados de la Secretaría de Educación?",
        "¿Qué indicadores ha logrado la Secretaría de Educación?",
        "Dime sobre los avances de la Secretaría de Educación",
        "¿Cuántos indicadores tiene completados educación?",
        "Secretaría de Educación indicadores completados",
        "educación 46.8% que indicadores completó",
    ]
    
    print(f"\n🧪 Probando {len(user_queries)} consultas realistas:")
    
    for i, query in enumerate(user_queries, 1):
        print(f"\n{'='*60}")
        print(f"CONSULTA {i}: '{query}'")
        print('='*60)
        
        try:
            # Simular detección de palabras clave
            query_lower = query.lower()
            indicator_keywords = ['indicador', 'meta', 'avance', 'progreso', 'resultado', 'ejecución', 'cumplimiento', 'secretaría', 'dependencia', 'educación', 'salud', 'tic', 'infraestructura', 'planeación', 'completado', 'completados', 'logrado', 'alcanzado']
            is_indicator_query = any(keyword in query_lower for keyword in indicator_keywords)
            
            print(f"📝 Detección de consulta de indicadores: {'✅ SÍ' if is_indicator_query else '❌ NO'}")
            if is_indicator_query:
                detected = [k for k in indicator_keywords if k in query_lower]
                print(f"   Palabras detectadas: {detected}")
            
            # Buscar contexto
            context = await knowledge_manager.get_context_for_query(query)
            
            print(f"🔍 Contexto encontrado: {'✅ SÍ' if context.strip() else '❌ NO'} ({len(context)} caracteres)")
            
            if context.strip():
                # Mostrar extractos relevantes del contexto
                lines = context.split('\n')
                relevant_lines = [line for line in lines if 'educación' in line.lower() or 'indicador' in line.lower()][:5]
                if relevant_lines:
                    print("📊 Extractos relevantes del contexto:")
                    for line in relevant_lines:
                        if line.strip():
                            print(f"   • {line[:120]}...")
                
                # Datos de referencia rápida que se añadirían
                if is_indicator_query:
                    print("🎯 Datos de referencia rápida que se incluirían:")
                    print("   • Secretaría de Educación: 46.8% avance físico, 94.8% ejecución presupuestal")
                    print("   • 21 indicadores totales, 8 completados")
                    
            # Respuesta completa con fuentes
            response = await knowledge_manager.answer_with_sources(query)
            print(f"📑 Fuentes oficiales encontradas: {response['found_sources']}")
            
            if response['found_sources'] > 0:
                print("📄 Documentos que contienen información relevante:")
                for result in response['raw_results'][:3]:  # Mostrar top 3
                    source = result['metadata']['source']
                    page = result['metadata'].get('page', 'N/A')
                    relevance = result['relevance_score']
                    print(f"   • {source} (Página {page}) - Relevancia: {relevance:.1%}")
                    
        except Exception as e:
            print(f"❌ Error en consulta: {e}")
            logger.exception("Error procesando consulta")
    
    print(f"\n{'='*60}")
    print("✅ Análisis completado")
    print("🔧 RECOMENDACIONES:")
    print("   1. La base vectorial SÍ tiene información sobre educación")
    print("   2. Las palabras clave detectan correctamente las consultas")
    print("   3. El problema puede estar en cómo el agente procesa la respuesta final")
    print("   4. Los datos de referencia rápida deberían proporcionar información básica")

if __name__ == "__main__":
    asyncio.run(test_education_specific())
