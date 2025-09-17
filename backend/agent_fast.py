#!/usr/bin/env python3
"""
Versión optimizada del agente para inicialización rápida en producción
"""
import os
import logging
import asyncio
from typing import List
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

logger = logging.getLogger("fast-agent")

class FastGovLabAssistant(Agent):
    def __init__(self) -> None:
        # Instrucciones mínimas para no exceder el límite de tokens de 'session.instructions'
        super().__init__(instructions=(
            "Eres Gober, asistente de Santander Territorio Inteligente. Sigue un tono claro y preciso,"
            " cita fuentes cuando sea posible, y nunca inventes cifras. Usa el contexto del sistema"
            " proporcionado en los mensajes previos para responder. Si falta una cifra exacta, dilo."
        ))
        
        # Carga perezosa del contexto completo desde archivo y lo divide en chunks pequeños
        self._context_chunks: List[str] = self._load_context_chunks()
        self._context_loaded = False

    def _load_context_chunks(self, max_chunk_chars: int = 3800) -> List[str]:
        """Lee el contexto extendido desde archivo y lo divide en chunks seguros.
        Devuelve una lista de strings (cada uno se envía como mensaje 'system')."""
        context_path = os.getenv(
            "GOBER_CONTEXT_FILE",
            os.path.join(os.path.dirname(__file__), "context", "agent_full_context.txt")
        )
        chunks: List[str] = []
        try:
            if os.path.exists(context_path):
                with open(context_path, "r", encoding="utf-8") as f:
                    data = f.read().strip()
                if not data:
                    return chunks
                # Normalizar saltos de línea largos y espacios extra
                data = "\n".join([line.rstrip() for line in data.splitlines()])
                # Partir por bloques cercanos a max_chunk_chars intentando respetar límites de párrafo
                start = 0
                while start < len(data):
                    end = min(start + max_chunk_chars, len(data))
                    # Intentar cortar en salto de línea cercano hacia atrás para no partir frases a la mitad
                    cut = data.rfind("\n\n", start, end)
                    if cut == -1 or cut <= start + 1000:  # si no hay buen corte, usa el end directon                        cut = end
                    chunk = data[start:cut].strip()
                    if chunk:
                        chunks.append(chunk)
                    start = cut
            else:
                logging.warning(f"Context file not found: {context_path}")
        except Exception as e:
            logging.warning(f"Failed to load context file: {e}")
        return chunks

    async def on_user_turn_completed(
        self,
        chat_ctx: llm.ChatContext,
        new_message: llm.ChatMessage
    ) -> None:
        # Keep the most recent 10 items for faster processing
        chat_ctx = chat_ctx.copy()
        if len(chat_ctx.items) > 10:
            chat_ctx.items = chat_ctx.items[-10:]
        
        # Carga el contexto completo (una sola vez) como mensajes 'system' para no saturar 'session.instructions'
        if not getattr(self, "_context_loaded", False) and self._context_chunks:
            try:
                for idx, chunk in enumerate(self._context_chunks, 1):
                    context_message = llm.ChatMessage.create(
                        text=f"[CONTEXTO {idx}/{len(self._context_chunks)}]\n" + chunk,
                        role="system"
                    )
                    chat_ctx.items.append(context_message)
                self._context_loaded = True
                logger.info(f"Loaded {len(self._context_chunks)} context chunks into chat context")
            except Exception as e:
                logger.warning(f"Failed loading context chunks: {e}")

        # Contexto ligero adicional según el tipo de consulta (sin base vectorial)
        if new_message.content:
            try:
                query_lower = new_message.content.lower()
                indicator_keywords = ['indicador', 'meta', 'avance', 'progreso', 'secretaría', 'educación', 'completado']
                is_indicator_query = any(keyword in query_lower for keyword in indicator_keywords)
                
                if is_indicator_query:
                    tip_message = llm.ChatMessage.create(
                        text="🎯 Para indicadores/metas usa los datos presentes en el contexto del sistema.",
                        role="system"
                    )
                    chat_ctx.items.append(tip_message)
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
