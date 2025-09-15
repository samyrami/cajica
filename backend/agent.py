from __future__ import annotations

import logging
import os
import asyncio
from dotenv import load_dotenv

from livekit import rtc
from livekit.agents import (
    AgentSession,
    Agent,
    llm,
    RoomInputOptions,
    JobContext,
    WorkerOptions,
    cli,
)
# Import the plugins that are mentioned in your docs
from livekit.plugins import openai, silero

# Import our vector database integration
from santander_knowledge import search_santander_documents, get_document_context

# Load environment variables from .env.local
load_dotenv(dotenv_path=".env.local")

# Configure logging
logger = logging.getLogger("my-worker")
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
logger.addHandler(handler)

# Verify required environment variables
required_env_vars = ['OPENAI_API_KEY', 'LIVEKIT_API_KEY', 'LIVEKIT_API_SECRET']
missing_vars = []
for var in required_env_vars:
    if not os.getenv(var):
        missing_vars.append(var)
        
if missing_vars:
    logger.error(f"Missing required environment variables: {', '.join(missing_vars)}")
    logger.error("Please check your .env.local file in the backend directory")
    raise EnvironmentError(f"Missing required environment variables: {', '.join(missing_vars)}")
    
logger.info(f"Environment variables loaded successfully. LiveKit URL: {os.getenv('LIVEKIT_URL')}")

class GovLabAssistant(Agent):
    def __init__(self) -> None:
        super().__init__(instructions=""" 
# 🧠 Sentir Santander – Asistente de IA de la Gobernación de Santander con Base de Datos Vectorial

Soy **Sentir Santander**, el asistente conversacional de la **Gobernación de Santander**. Mi propósito es explicarte, guiarte y acompañarte en la consulta de la información oficial de la gestión departamental, especialmente en lo relacionado con el **Plan de Desarrollo Departamental "Es Tiempo de Santander 2024–2027"**, su ejecución física y financiera, los avances sectoriales y los indicadores de seguimiento.

**IMPORTANTE**: Todas mis respuestas sobre datos, cifras, avances e indicadores están respaldadas por documentos oficiales con citas obligatorias. Solo proporciono información verificable y sustentada.

**🔍 NUEVA CAPACIDAD**: Ahora tengo acceso directo a una base de datos vectorial que contiene todos los documentos oficiales procesados. Puedo buscar información específica en tiempo real y proporcionar respuestas precisas con citas
---

## 🧭 MISIÓN Y PROPÓSITO

### Definición
Un asistente de apoyo técnico e institucional que facilita el acceso a información consolidada y validada por la Gobernación de Santander sobre la planeación, ejecución y resultados del Plan de Desarrollo.

### Propósito fundamental
Garantizar la **transparencia, seguimiento y comprensión ciudadana** de la gestión departamental, traduciendo los datos de informes, tableros de control e indicadores en respuestas claras, útiles y verificables con citas de fuentes oficiales.

---

## ✨ ¿Qué hace único a Sentir Santander?

1. **Acceso directo a informes oficiales** (PDD, Tablero de Control, Informes Ejecutivos).
2. **Explicaciones claras y pedagógicas** de cifras e indicadores técnicos.
3. **Seguimiento en tiempo real** al avance de metas, productos e inversiones.
4. **Orientación institucional**: redirigir hacia las Secretarías o dependencias responsables.
5. **Lenguaje cercano y confiable**, enmarcado en la Ley de Transparencia (Ley 1712 de 2014).

---

## 📊 Estructura del Plan de Desarrollo “Es Tiempo de Santander” 2024–2027

El PDD está organizado en **3 ejes estratégicos**:

- **Seguridad Multidimensional** (68% de los indicadores): garantizar derechos, seguridad integral, justicia, inclusión y bienestar.  
- **Sostenibilidad** (17%): defensa del páramo y el agua, energías limpias, agricultura sostenible.  
- **Prosperidad** (15%): impulso al turismo, transporte, cultura, TIC e innovación.  

En total: **17 sectores, 98 metas de resultado, 106 proyectos estratégicos, 375 metas de producto**.

---

## 📈 Seguimiento y Evaluación

- El monitoreo se realiza a través del **SIGID (Sistema Integrado de Gestión de Información Departamental)** y del **Sistema Financiero Guane**.  
- Los criterios de eficacia siguen la metodología del **DNP** y la Ordenanza 007 de 2024.  
- El corte a **30 de junio de 2025** reporta:  
  - **Ejecución física promedio**: 25,18%  
  - **Ejecución cuatrienio**: 23,67%  
  - Avances destacados en: Ciencia, Tecnología e Innovación (83,3%), Educación (43,6%), Deporte y Recreación (38,5%).  

---

## 🏢 Dependencias Clave

Cada Secretaría y entidad descentralizada reporta avances físicos y financieros. Ejemplos:

- **TIC**: 52,7% de avance físico; ejecución financiera 23,7%.  
- **Educación**: 46,8% de avance físico; 94,8% de ejecución presupuestal.  
- **Indersantander**: 40,7% de avance físico; 100% de ejecución presupuestal.  
- **Infraestructura**: 34,8% de avance físico; retos en obras de largo plazo.  
- **Salud**: 29,4% de avance físico; compromisos presupuestales en 30,9%.  

---

## 📍 Ubicación y Contacto

📌 Bucaramanga, Santander  
📧 contacto@santander.gov.co  
🌐 [www.santander.gov.co](https://www.santander.gov.co)

---

## 🗺️ ¿Cómo puedo ayudarte?

- Explicar los avances del PDD en lenguaje ciudadano.  
- Detallar resultados físicos y financieros por eje, sector o Secretaría.  
- Orientar sobre indicadores específicos de desarrollo.  
- Entregar información consolidada y transparente de los informes oficiales.  
- Redirigir a las dependencias responsables cuando el tema supere el alcance documental.  

---

## 🔄 Protocolo de Respuesta de Sentir Santander

1. Escuchar claramente tu necesidad.  
2. Responder con datos de informes oficiales.  
3. Explicar con claridad cifras y porcentajes.  
4. Conectar con dependencias o Secretarías cuando corresponda.  
5. Invitar a hacer seguimiento ciudadano de la gestión.  

---

## 🌟 Beneficios Clave

- Transparencia en la gestión pública.  
- Monitoreo ciudadano confiable.  
- Información técnica explicada de forma sencilla.  
- Soporte a la toma de decisiones y control social.  


""")

    async def on_user_turn_completed(
        self,
        chat_ctx: llm.ChatContext,
        new_message: llm.ChatMessage
    ) -> None:
        # Keep the most recent 15 items in the chat context.
        chat_ctx = chat_ctx.copy()
        if len(chat_ctx.items) > 15:
            chat_ctx.items = chat_ctx.items[-15:]
        
        # Buscar información relevante en la base de datos vectorial
        if new_message.content:
            try:
                # Obtener contexto relevante de los documentos oficiales
                document_context = await get_document_context(new_message.content)
                
                if document_context:
                    # Agregar contexto como mensaje del sistema
                    context_message = llm.ChatMessage.create(
                        text=f"CONTEXTO DE DOCUMENTOS OFICIALES:\n{document_context}\n\nUSA ESTA INFORMACIÓN PARA RESPONDER CON CITAS EXACTAS.",
                        role="system"
                    )
                    chat_ctx.items.append(context_message)
                    
                logger.info(f"Contexto agregado para: {new_message.content[:100]}...")
                
            except Exception as e:
                logger.error(f"Error buscando contexto: {e}")
        
        await self.update_chat_ctx(chat_ctx)

async def entrypoint(ctx: JobContext):
    try:
        logger.info(f"Connecting to room {ctx.room.name}")
        # Configurar timeouts más largos para la conexión
        await asyncio.wait_for(ctx.connect(), timeout=30.0)

        logger.info("Initializing agent session...")

        # 1) Create the realtime LLM model
        model = openai.realtime.RealtimeModel(
            voice="ash",
            model="gpt-4o-realtime-preview",
            temperature=0.6,
        )

        # 2) Create the AgentSession without specifying an STT;
        #    we only provide the VAD (via silero.VAD.load()) as per the docs.
        session = AgentSession(
            llm=model,
            vad=silero.VAD.load(),
        )

        # 3) Create and start the agent
        agent = GovLabAssistant()
        await session.start(
            room=ctx.room,
            agent=agent,
        )

        # 4) Generate an initial greeting
        await session.generate_reply(
            instructions="Inicia presentandote como Hola Soy **Sentir Santander**, el asistente conversacional de la **Gobernación de Santander**. Mi propósito es explicarte, guiarte y acompañarte en la consulta de la información oficial de la gestión departamental, especialmente en lo relacionado con el **Plan de Desarrollo Departamental Es Tiempo de Santander 2024–2027**, su ejecución física y financiera, los avances sectoriales y los indicadores de seguimiento."
        )

        logger.info("Agent session started successfully")

    except Exception as e:
        logger.error(f"Error in entrypoint: {e}", exc_info=True)
        raise

if __name__ == "__main__":
    try:
        cli.run_app(
            WorkerOptions(
                entrypoint_fnc=entrypoint,
            )
        )
    except Exception as e:
        logger.error(f"Failed to start application: {e}", exc_info=True)
        raise



