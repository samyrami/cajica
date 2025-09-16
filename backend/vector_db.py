"""
Gestor de Base de Datos Vectorial para Gober
======================================================

Este módulo maneja la creación, carga y consulta de documentos 
en una base de datos vectorial usando ChromaDB.

Características:
- Procesamiento de PDFs y archivos Excel
- Embeddings multilingües optimizados para español
- Búsqueda semántica con metadatos contextuales
- Integración con el agente conversacional
"""

import os
import logging
from typing import List, Dict, Any, Optional, Tuple
import chromadb
from chromadb.config import Settings
import pandas as pd
from PyPDF2 import PdfReader
from sentence_transformers import SentenceTransformer
import hashlib
import json
from datetime import datetime
import uuid

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SantanderVectorDB:
    """
    Gestor de base de datos vectorial para documentos de Santander Territorio inteligente
    """
    
    def __init__(self, data_dir: str = "./data", db_dir: str = "./chroma_db"):
        """
        Inicializa la base de datos vectorial
        
        Args:
            data_dir (str): Directorio donde están los documentos fuente
            db_dir (str): Directorio donde se almacena la base de datos vectorial
        """
        self.data_dir = data_dir
        self.db_dir = db_dir
        
        # Crear directorios si no existen
        os.makedirs(self.db_dir, exist_ok=True)
        
        # Inicializar ChromaDB
        self.client = chromadb.PersistentClient(path=self.db_dir)
        
        # Inicializar el modelo de embeddings (optimizado para español)
        logger.info("Cargando modelo de embeddings...")
        self.embedding_model = SentenceTransformer('sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2')
        
        # Obtener o crear la colección
        self.collection_name = "santander_documents"
        try:
            self.collection = self.client.get_collection(name=self.collection_name)
            logger.info(f"Colección '{self.collection_name}' cargada exitosamente")
        except:
            logger.info(f"Creando nueva colección '{self.collection_name}'")
            self.collection = self.client.create_collection(
                name=self.collection_name,
                metadata={"description": "Documentos oficiales de la Gobernación de Santander"}
            )
    
    def _generate_chunk_id(self, content: str, metadata: Dict[str, Any]) -> str:
        """
        Genera un ID único para cada chunk basado en el contenido y metadatos
        
        Args:
            content (str): Contenido del chunk
            metadata (dict): Metadatos del chunk
            
        Returns:
            str: ID único para el chunk
        """
        content_hash = hashlib.md5(content.encode()).hexdigest()
        source_info = f"{metadata.get('source', 'unknown')}_{metadata.get('page', 0)}"
        return f"{source_info}_{content_hash[:8]}"
    
    def _process_pdf_document(self, file_path: str) -> List[Dict[str, Any]]:
        """
        Procesa un documento PDF y extrae texto por páginas
        
        Args:
            file_path (str): Ruta al archivo PDF
            
        Returns:
            List[Dict]: Lista de chunks con contenido y metadatos
        """
        chunks = []
        
        try:
            reader = PdfReader(file_path)
            file_name = os.path.basename(file_path)
            
            logger.info(f"Procesando PDF: {file_name} ({len(reader.pages)} páginas)")
            
            for page_num, page in enumerate(reader.pages, 1):
                text = page.extract_text()
                
                # Limpiar y dividir el texto en chunks más pequeños
                if text.strip():
                    # Dividir por párrafos largos
                    paragraphs = text.split('\n\n')
                    
                    current_chunk = ""
                    for paragraph in paragraphs:
                        # Si agregar este párrafo no excede el límite, agregarlo
                        if len(current_chunk + paragraph) < 1000:
                            current_chunk += paragraph + "\n\n"
                        else:
                            # Guardar el chunk actual si no está vacío
                            if current_chunk.strip():
                                chunk_metadata = {
                                    "source": file_name,
                                    "source_type": "pdf",
                                    "page": page_num,
                                    "document_type": self._classify_document_type(file_name),
                                    "processed_at": datetime.now().isoformat()
                                }
                                
                                chunks.append({
                                    "content": current_chunk.strip(),
                                    "metadata": chunk_metadata
                                })
                            
                            # Empezar nuevo chunk
                            current_chunk = paragraph + "\n\n"
                    
                    # Agregar el último chunk si no está vacío
                    if current_chunk.strip():
                        chunk_metadata = {
                            "source": file_name,
                            "source_type": "pdf", 
                            "page": page_num,
                            "document_type": self._classify_document_type(file_name),
                            "processed_at": datetime.now().isoformat()
                        }
                        
                        chunks.append({
                            "content": current_chunk.strip(),
                            "metadata": chunk_metadata
                        })
        
        except Exception as e:
            logger.error(f"Error procesando PDF {file_path}: {e}")
        
        return chunks
    
    def _process_excel_document(self, file_path: str) -> List[Dict[str, Any]]:
        """
        Procesa un archivo Excel y convierte los datos en chunks textuales
        
        Args:
            file_path (str): Ruta al archivo Excel
            
        Returns:
            List[Dict]: Lista de chunks con contenido y metadatos
        """
        chunks = []
        file_name = os.path.basename(file_path)
        
        try:
            # Leer todas las hojas del archivo Excel
            excel_file = pd.ExcelFile(file_path)
            
            logger.info(f"Procesando Excel: {file_name} ({len(excel_file.sheet_names)} hojas)")
            
            for sheet_name in excel_file.sheet_names:
                df = pd.read_excel(file_path, sheet_name=sheet_name)
                
                # Convertir DataFrame a texto estructurado
                if not df.empty:
                    # Crear resumen de la hoja
                    sheet_summary = f"Hoja: {sheet_name}\nColumnas: {', '.join(df.columns.astype(str))}\nFilas: {len(df)}\n\n"
                    
                    # Procesar por bloques de filas
                    chunk_size = 50
                    for i in range(0, len(df), chunk_size):
                        chunk_df = df.iloc[i:i+chunk_size]
                        
                        # Convertir a texto estructurado
                        text_content = sheet_summary
                        text_content += f"Datos (filas {i+1} a {min(i+chunk_size, len(df))}):\n"
                        
                        for idx, row in chunk_df.iterrows():
                            row_text = " | ".join([f"{col}: {val}" for col, val in row.items() if pd.notna(val)])
                            text_content += f"- {row_text}\n"
                        
                        chunk_metadata = {
                            "source": file_name,
                            "source_type": "excel",
                            "sheet": sheet_name,
                            "row_range": f"{i+1}-{min(i+chunk_size, len(df))}",
                            "document_type": self._classify_document_type(file_name),
                            "processed_at": datetime.now().isoformat()
                        }
                        
                        chunks.append({
                            "content": text_content,
                            "metadata": chunk_metadata
                        })
        
        except Exception as e:
            logger.error(f"Error procesando Excel {file_path}: {e}")
        
        return chunks
    
    def _classify_document_type(self, filename: str) -> str:
        """
        Clasifica el tipo de documento basado en el nombre del archivo
        
        Args:
            filename (str): Nombre del archivo
            
        Returns:
            str: Tipo de documento clasificado
        """
        filename_lower = filename.lower()
        
        if "informe" in filename_lower and "gestion" in filename_lower:
            return "informe_gestion"
        elif "informe" in filename_lower and "ejecutivo" in filename_lower:
            return "informe_ejecutivo"
        elif "tablero" in filename_lower and "control" in filename_lower:
            return "tablero_control"
        elif filename_lower.endswith(".xlsx") and filename_lower.startswith("6"):
            return "datos_complementarios"
        else:
            return "documento_general"
    
    def load_documents(self) -> None:
        """
        Carga todos los documentos del directorio de datos a la base vectorial
        """
        logger.info(f"Iniciando carga de documentos desde: {self.data_dir}")
        
        all_chunks = []
        
        # Procesar archivos PDF
        for filename in os.listdir(self.data_dir):
            file_path = os.path.join(self.data_dir, filename)
            
            if filename.lower().endswith('.pdf'):
                chunks = self._process_pdf_document(file_path)
                all_chunks.extend(chunks)
            elif filename.lower().endswith(('.xlsx', '.xls')):
                chunks = self._process_excel_document(file_path)
                all_chunks.extend(chunks)
        
        if all_chunks:
            logger.info(f"Procesando {len(all_chunks)} chunks para vectorización...")
            
            # Preparar datos para ChromaDB
            documents = []
            metadatas = []
            ids = []
            
            for chunk in all_chunks:
                documents.append(chunk["content"])
                metadatas.append(chunk["metadata"])
                ids.append(self._generate_chunk_id(chunk["content"], chunk["metadata"]))
            
            # Generar embeddings
            logger.info("Generando embeddings...")
            embeddings = self.embedding_model.encode(documents, convert_to_tensor=False)
            
            # Agregar a ChromaDB
            logger.info("Guardando en base de datos vectorial...")
            self.collection.upsert(
                documents=documents,
                metadatas=metadatas,
                ids=ids,
                embeddings=embeddings.tolist()
            )
            
            logger.info(f"✅ Carga completada: {len(all_chunks)} chunks almacenados")
        else:
            logger.warning("No se encontraron documentos válidos para procesar")
    
    def search(self, query: str, n_results: int = 5, document_type: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Realiza búsqueda semántica en la base de datos vectorial
        
        Args:
            query (str): Consulta de búsqueda
            n_results (int): Número de resultados a devolver
            document_type (str, optional): Filtro por tipo de documento
            
        Returns:
            List[Dict]: Resultados de búsqueda con contenido, metadatos y scores
        """
        logger.info(f"Realizando búsqueda: '{query}' (límite: {n_results})")
        
        # Preparar filtros si se especifica tipo de documento
        where_filter = None
        if document_type:
            where_filter = {"document_type": document_type}
        
        # Realizar búsqueda
        results = self.collection.query(
            query_texts=[query],
            n_results=n_results,
            where=where_filter
        )
        
        # Formatear resultados
        formatted_results = []
        if results['documents'] and results['documents'][0]:
            for i in range(len(results['documents'][0])):
                formatted_results.append({
                    "content": results['documents'][0][i],
                    "metadata": results['metadatas'][0][i],
                    "distance": results['distances'][0][i],
                    "relevance_score": 1 - results['distances'][0][i]  # Convertir distancia a score de relevancia
                })
        
        logger.info(f"Encontrados {len(formatted_results)} resultados")
        return formatted_results
    
    def get_document_stats(self) -> Dict[str, Any]:
        """
        Obtiene estadísticas de los documentos almacenados
        
        Returns:
            Dict: Estadísticas de la base de datos
        """
        try:
            count = self.collection.count()
            
            # Obtener una muestra para analizar tipos de documentos
            sample = self.collection.get(limit=1000)
            
            doc_types = {}
            sources = set()
            
            if sample['metadatas']:
                for metadata in sample['metadatas']:
                    doc_type = metadata.get('document_type', 'unknown')
                    doc_types[doc_type] = doc_types.get(doc_type, 0) + 1
                    sources.add(metadata.get('source', 'unknown'))
            
            return {
                "total_chunks": count,
                "document_types": doc_types,
                "unique_sources": len(sources),
                "sources_list": list(sources)
            }
        except Exception as e:
            logger.error(f"Error obteniendo estadísticas: {e}")
            return {"error": str(e)}
    
    def clear_database(self) -> bool:
        """
        Limpia completamente la base de datos vectorial
        
        Returns:
            bool: True si la operación fue exitosa
        """
        try:
            # Eliminar colección actual
            self.client.delete_collection(name=self.collection_name)
            
            # Recrear colección vacía
            self.collection = self.client.create_collection(
                name=self.collection_name,
                metadata={"description": "Documentos oficiales de la Gobernación de Santander"}
            )
            
            logger.info("Base de datos vectorial limpiada exitosamente")
            return True
        except Exception as e:
            logger.error(f"Error limpiando base de datos: {e}")
            return False

def main():
    """
    Función principal para pruebas del módulo
    """
    # Inicializar base de datos
    db = SantanderVectorDB()
    
    # Mostrar estadísticas actuales
    stats = db.get_document_stats()
    print(f"📊 Estadísticas actuales: {stats}")
    
    # Cargar documentos
    db.load_documents()
    
    # Mostrar estadísticas después de la carga
    new_stats = db.get_document_stats()
    print(f"📊 Estadísticas después de la carga: {new_stats}")
    
    # Realizar búsqueda de prueba
    results = db.search("Plan de Desarrollo Departamental", n_results=3)
    print(f"\n🔍 Resultados de búsqueda de prueba:")
    for i, result in enumerate(results, 1):
        print(f"{i}. Score: {result['relevance_score']:.3f}")
        print(f"   Fuente: {result['metadata']['source']}")
        print(f"   Contenido: {result['content'][:100]}...")
        print()

if __name__ == "__main__":
    main()
