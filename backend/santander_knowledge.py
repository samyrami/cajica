"""
Módulo de Conocimiento para Gober
============================================

Este módulo maneja la integración entre el agente conversacional 
y la base de datos vectorial de documentos oficiales.
"""

import logging
from typing import List, Dict, Any, Optional
from vector_db import SantanderVectorDB
import asyncio

logger = logging.getLogger(__name__)

class SantanderKnowledge:
    """
    Gestor de conocimiento que integra la base de datos vectorial
    con el agente conversacional de Gober
    """
    
    def __init__(self, data_dir: str = "./data", db_dir: str = "./chroma_db"):
        """
        Inicializa el gestor de conocimiento
        
        Args:
            data_dir (str): Directorio de documentos fuente
            db_dir (str): Directorio de la base de datos vectorial
        """
        self.vector_db = SantanderVectorDB(data_dir=data_dir, db_dir=db_dir)
        self.is_loaded = False
        
    async def ensure_loaded(self):
        """
        Asegura que la base de datos esté cargada antes de realizar consultas
        """
        if not self.is_loaded:
            stats = self.vector_db.get_document_stats()
            if stats.get("total_chunks", 0) == 0:
                logger.info("Base de datos vacía, cargando documentos...")
                await asyncio.get_event_loop().run_in_executor(
                    None, self.vector_db.load_documents
                )
            self.is_loaded = True
    
    async def search_documents(
        self, 
        query: str, 
        n_results: int = 3, 
        document_type: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Busca información relevante en los documentos oficiales
        
        Args:
            query (str): Consulta de búsqueda
            n_results (int): Número máximo de resultados
            document_type (str, optional): Tipo específico de documento
            
        Returns:
            List[Dict]: Resultados de búsqueda con contenido y metadatos
        """
        await self.ensure_loaded()
        
        # Realizar búsqueda en la base de datos vectorial
        results = await asyncio.get_event_loop().run_in_executor(
            None, 
            self.vector_db.search, 
            query, 
            n_results, 
            document_type
        )
        
        return results
    
    def format_search_results(self, results: List[Dict[str, Any]], query: str) -> str:
        """
        Formatea los resultados de búsqueda para el agente conversacional
        
        Args:
            results (List[Dict]): Resultados de la búsqueda vectorial
            query (str): Consulta original
            
        Returns:
            str: Texto formateado con la información encontrada
        """
        if not results:
            return f"No encontré información específica sobre '{query}' en los documentos oficiales disponibles."
        
        # Construir respuesta estructurada
        response_parts = []
        response_parts.append(f"📋 **Información encontrada sobre '{query}':**\n")
        
        for i, result in enumerate(results, 1):
            metadata = result['metadata']
            content = result['content']
            score = result['relevance_score']
            
            # Determinar tipo de documento para el emoji
            doc_type = metadata.get('document_type', 'unknown')
            emoji = self._get_document_emoji(doc_type)
            
            # Formatear entrada
            source_info = f"{emoji} **{metadata['source']}**"
            
            if metadata.get('page'):
                source_info += f" (Página {metadata['page']})"
            elif metadata.get('sheet'):
                source_info += f" (Hoja: {metadata['sheet']})"
            
            # Truncar contenido si es muy largo
            display_content = content[:400] + "..." if len(content) > 400 else content
            
            response_parts.append(f"\n**{i}. {source_info}**")
            response_parts.append(f"*Relevancia: {score:.1%}*")
            response_parts.append(f"{display_content}")
            response_parts.append("---")
        
        # Agregar nota sobre fuentes oficiales
        response_parts.append("\n✅ **Toda esta información proviene de documentos oficiales de la Gobernación de Santander**")
        
        return "\n".join(response_parts)
    
    def _get_document_emoji(self, document_type: str) -> str:
        """
        Retorna emoji apropiado según el tipo de documento
        
        Args:
            document_type (str): Tipo de documento
            
        Returns:
            str: Emoji correspondiente
        """
        emoji_map = {
            "informe_gestion": "📊",
            "informe_ejecutivo": "📄", 
            "tablero_control": "📈",
            "datos_complementarios": "📋",
            "documento_general": "📝"
        }
        
        return emoji_map.get(document_type, "📄")
    
    async def get_context_for_query(self, query: str) -> str:
        """
        Obtiene contexto relevante para una consulta específica (optimizado para velocidad)
        
        Args:
            query (str): Consulta del usuario
            
        Returns:
            str: Contexto relevante para la respuesta
        """
        # Buscar información relevante con menos resultados para mayor velocidad
        results = await self.search_documents(query, n_results=2)
        
        if results:
            # Extraer solo el contenido más relevante para usar como contexto
            context_parts = []
            for i, result in enumerate(results, 1):
                metadata = result['metadata']
                content = result['content']
                
                # Incluir fuente exacta con página si está disponible
                source_citation = f"FUENTE {i}: {metadata['source']}"
                if metadata.get('page'):
                    source_citation += f" - Página {metadata['page']}"
                elif metadata.get('sheet'):
                    source_citation += f" - Hoja: {metadata['sheet']}"
                
                context_parts.append(source_citation)
                context_parts.append(content)
                context_parts.append("---")
            
            return "\n".join(context_parts)
        
        return ""
    
    async def answer_with_sources(self, query: str) -> Dict[str, Any]:
        """
        Proporciona una respuesta completa con fuentes citadas
        
        Args:
            query (str): Pregunta del usuario
            
        Returns:
            Dict: Respuesta estructurada con contenido y metadatos
        """
        results = await self.search_documents(query, n_results=5)
        
        response = {
            "query": query,
            "found_sources": len(results),
            "formatted_response": self.format_search_results(results, query),
            "raw_results": results,
            "has_official_data": len(results) > 0
        }
        
        return response
    
    def get_stats(self) -> Dict[str, Any]:
        """
        Obtiene estadísticas de la base de conocimiento
        
        Returns:
            Dict: Estadísticas de documentos disponibles
        """
        return self.vector_db.get_document_stats()

# Instancia global para usar en el agente
knowledge_manager = SantanderKnowledge()

async def search_santander_documents(query: str, max_results: int = 3) -> str:
    """
    Función de conveniencia para buscar en documentos de Santander
    
    Args:
        query (str): Consulta de búsqueda
        max_results (int): Máximo número de resultados
        
    Returns:
        str: Respuesta formateada
    """
    response = await knowledge_manager.answer_with_sources(query)
    return response["formatted_response"]

async def get_document_context(query: str) -> str:
    """
    Función de conveniencia para obtener contexto de documentos
    
    Args:
        query (str): Consulta de búsqueda
        
    Returns:
        str: Contexto relevante
    """
    return await knowledge_manager.get_context_for_query(query)
