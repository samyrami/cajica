#!/usr/bin/env python3
"""
Versión optimizada del agente para inicialización rápida en producción
"""
import os
import logging
import asyncio
from dotenv import load_dotenv

# Optimizar configuración de logging para producción
logging.basicConfig(
    level=logging.WARNING,  # Solo errores y advertencias
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Load environment variables
load_dotenv(dotenv_path=".env.local")

# Import después de configurar logging
from livekit import rtc
from livekit.agents import (
    AgentSession,
    Agent,
    llm,
    JobContext,
    WorkerOptions,
    cli,
)
from livekit.plugins import openai, silero

# Import lazy loading functions
from santander_knowledge import get_document_context

logger = logging.getLogger("fast-agent")

class FastGovLabAssistant(Agent):
    def __init__(self) -> None:
        # Mismo contenido de instrucciones, pero más conciso para inicialización
        super().__init__(instructions=""" 
# 🧠 Gober – Asistente de Santander Territorio inteligente

Soy **Gober**, el asistente de **Santander Territorio inteligente** para consultas sobre el **Plan de Desarrollo "Es Tiempo de Santander 2024–2027"**.

## 📊 DATOS DE SECRETARÍAS (ACTUALIZADOS):

- **Educación**: 46.8% avance físico, 94.8% ejecución presupuestal, 21 indicadores totales, 8 completados
- **TIC**: 48.8% avance físico, 10 indicadores totales, 3 completados  
- **Indersantander**: 43.65% avance físico, 14 indicadores totales, 4 completados
- **Planeación**: 43.02% avance físico, 19 indicadores totales, 8 completados
- **Infraestructura**: 22.8% avance físico, 53 indicadores totales, 15 completados
- **Salud**: 26.89% avance físico, 54 indicadores totales, 12 completados

## ⚠️ PROTOCOLO CRÍTICO:
1. SIEMPRE usar datos específicos de arriba para preguntas sobre indicadores/metas
2. Los porcentajes son PROMEDIOS de avance por secretaría
3. Plan tiene 98 metas, 17 sectores, 3 ejes estratégicos
4. Citar fuentes cuando sea posible

## 🎯 SALUDO: "¡Hola! Soy Gober, el asistente virtual de Santander Territorio inteligente. Puedes preguntarme sobre los objetivos estratégicos y avances del departamento. ¿En qué puedo ayudarte hoy?"

""")

    async def on_user_turn_completed(
        self,
        chat_ctx: llm.ChatContext,
        new_message: llm.ChatMessage
    ) -> None:
        # Keep the most recent 10 items for faster processing
        chat_ctx = chat_ctx.copy()
        if len(chat_ctx.items) > 10:
            chat_ctx.items = chat_ctx.items[-10:]
        
        # Búsqueda vectorial optimizada
        if new_message.content:
            try:
                query_lower = new_message.content.lower()
                indicator_keywords = ['indicador', 'meta', 'avance', 'progreso', 'secretaría', 'educación', 'completado']
                is_indicator_query = any(keyword in query_lower for keyword in indicator_keywords)
                
                logger.info(f"Query type indicator: {is_indicator_query}")
                
                # Contexto mínimo pero efectivo
                additional_context = ""
                if is_indicator_query:
                    additional_context = "\n🎯 RESPONDE CON DATOS ESPECÍFICOS DE LAS SECRETARÍAS EN TUS INSTRUCCIONES."
                
                # Solo buscar en DB si realmente necesario
                document_context = ""
                if "específico" in query_lower or "detalle" in query_lower:
                    try:
                        document_context = await get_document_context(new_message.content)
                    except Exception as e:
                        logger.warning(f"Vector DB not available: {e}")
                
                # Contexto simplificado
                full_context = f"CONTEXTO: {additional_context}\nUSA TUS CONOCIMIENTOS SOBRE SANTANDER PARA RESPONDER CON PRECISIÓN."
                context_message = llm.ChatMessage.create(
                    text=full_context,
                    role="system"
                )
                chat_ctx.items.append(context_message)
                
            except Exception as e:
                logger.error(f"Context error: {e}")
        
        await self.update_chat_ctx(chat_ctx)

async def fast_entrypoint(ctx: JobContext):
    try:
        logger.info("Fast initialization starting...")
        
        # Conexión rápida con timeout extendido
        await asyncio.wait_for(ctx.connect(), timeout=45.0)

        # Modelo optimizado
        model = openai.realtime.RealtimeModel(
            voice="ash",
            model="gpt-4o-realtime-preview",
            temperature=0.3,
        )

        # VAD con configuración mínima
        vad = silero.VAD.load()
        
        session = AgentSession(llm=model, vad=vad)

        # Agente optimizado
        agent = FastGovLabAssistant()
        await session.start(room=ctx.room, agent=agent)

        # Saludo directo
        await session.generate_reply(
            instructions="Di exactamente: '¡Hola! Soy Gober, el asistente virtual de Santander Territorio inteligente. Puedes preguntarme sobre los objetivos estratégicos y avances del departamento. ¿En qué puedo ayudarte hoy?'"
        )

        logger.info("Fast agent ready")

    except Exception as e:
        logger.error(f"Fast startup error: {e}")
        raise

if __name__ == "__main__":
    cli.run_app(WorkerOptions(entrypoint_fnc=fast_entrypoint))
