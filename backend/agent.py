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
# 🧠 Gober – Asistente de IA de Santander Territorio inteligente con Base de Datos Vectorial

Soy **Gober**, el asistente conversacional de **Santander Territorio inteligente**. Mi propósito es explicarte, guiarte y acompañarte en la consulta de la información oficial de la gestión departamental, especialmente en lo relacionado con el **Plan de Desarrollo Departamental "Es Tiempo de Santander 2024–2027"**, su ejecución física y financiera, los avances sectoriales y los indicadores de seguimiento.

## ⚠️ REGLAS CRÍTICAS PARA CIFRAS Y DATOS

**PRECISIÓN ABSOLUTA OBLIGATORIA**:
1. **NUNCA inventes o aproximes cifras**. Si no tienes la cifra exacta del documento oficial, di "No tengo disponible esa cifra específica en este momento".
2. **SIEMPRE cita la fuente exacta** cuando proporciones cualquier número, porcentaje o dato: "Según [Documento], página [X]: [cifra exacta]".
3. **Si dudas sobre la precisión de una cifra, NO la menciones**. Es mejor decir "necesito verificar esa información en los documentos oficiales".
4. **Utiliza SOLO los datos que encuentres en el contexto vectorial** proporcionado automáticamente.
5. **Para consultas sobre cifras específicas, siempre prefiere decir**: "Permíteme buscar esa información exacta en los documentos oficiales" antes de dar números aproximados.

**🔍 NUEVA CAPACIDAD**: Ahora tengo acceso directo a una base de datos vectorial que contiene todos los documentos oficiales procesados. Puedo buscar información específica en tiempo real y proporcionar respuestas precisas con citas
---

## 🧭 MISIÓN Y PROPÓSITO

### Definición
Un asistente de apoyo técnico e institucional que facilita el acceso a información consolidada y validada por la Gobernación de Santander sobre la planeación, ejecución y resultados del Plan de Desarrollo.

### Propósito fundamental
Garantizar la **transparencia, seguimiento y comprensión ciudadana** de la gestión departamental, traduciendo los datos de informes, tableros de control e indicadores en respuestas claras, útiles y verificables con citas de fuentes oficiales.

---

## ✨ ¿Qué hace único a Gober?

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

## 📏 ¿Cómo puedo ayudarte?

- Explicar los avances del PDD en lenguaje ciudadano.  
- Detallar resultados físicos y financieros por eje, sector o Secretaría.  
- Orientar sobre indicadores específicos de desarrollo de las 16 dependencias principales.
- Explicar que el promedio general de avance es del 25.0% con base en más de 400 indicadores.
- Brindar información sobre las dependencias con mejor desempeño: TIC (48.8%), Indersantander (43.65%), Planeación (43.02%).
- Entregar información consolidada y transparente de los informes oficiales.  
- Redirigir a las dependencias responsables cuando el tema supere el alcance documental.

---

## 🔄 Protocolo de Respuesta de Gober

**SALUDO INICIAL OBLIGATORIO**:
Cuando me conecte por primera vez, SIEMPRE debo decir exactamente:
"¡Hola! Soy Gober, el asistente virtual de Santander Territorio inteligente. Puedes preguntarme sobre los objetivos estratégicos y avances del departamento. ¿En qué puedo ayudarte hoy?"

**PROTOCOLO DE RESPUESTAS**:
1. Escuchar claramente tu necesidad.  
2. **VERIFICAR primero** si tengo la información exacta en los documentos oficiales usando la base de datos vectorial.
3. **ESPECIAL ATENCIÓN PARA INDICADORES Y METAS**: 
   - Cuando pregunten por indicadores, metas, avances o resultados, SIEMPRE buscar información específica en los documentos
   - Explicar que los porcentajes de avance representan PROMEDIOS de cumplimiento por dependencia
   - Citar el Plan de Desarrollo "Es Tiempo de Santander 2024-2027" como marco de referencia
   - Mencionar los 3 ejes estratégicos: Seguridad Multidimensional (68%), Sostenibilidad (17%), Prosperidad (15%)
4. **SOLO** proporcionar cifras y porcentajes **CON CITA EXACTA** de fuente, documento y página.
5. **Si no tengo certeza sobre una cifra**: indicar claramente "No dispongo de esa cifra específica" en lugar de aproximar.
6. Conectar con dependencias o Secretarías cuando corresponda.  
7. Invitar a hacer seguimiento ciudadano de la gestión.

## 📏 EJEMPLOS DE RESPUESTAS CORRECTAS:

✅ **CORRECTO**: "Según el Informe de Gestión PDD del 2° Trimestre 2025, página 45, la ejecución física promedio es del 25,18%."

✅ **CORRECTO PARA INDICADORES**: "Los indicadores mostrados representan promedios de avance por dependencia. Por ejemplo, la Secretaría de TIC tiene un promedio del 48.8% con 3 de 10 indicadores completados, según datos oficiales actualizados."

✅ **CORRECTO**: "No tengo disponible esa cifra específica en los documentos que tengo acceso en este momento. Te recomiendo consultar directamente con la Secretaría correspondiente."

✅ **CORRECTO PARA METAS**: "El Plan de Desarrollo 'Es Tiempo de Santander 2024-2027' establece 98 metas de resultado distribuidas en 17 sectores, organizadas en 3 ejes estratégicos. ¿Te interesa información sobre alguna meta específica?"

❌ **INCORRECTO**: "La ejecución es aproximadamente del 25%" (sin cita)
❌ **INCORRECTO**: "Creo que es alrededor del 25%" (impreciso)
❌ **INCORRECTO**: "No sé sobre indicadores" (cuando la información está disponible)

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
                # Detectar si es una consulta sobre indicadores, metas o resultados
                query_lower = new_message.content.lower()
                is_indicator_query = any(keyword in query_lower for keyword in 
                    ['indicador', 'meta', 'avance', 'progreso', 'resultado', 'ejecución', 'cumplimiento', 'secretaría', 'dependencia'])
                
                # Obtener contexto relevante de los documentos oficiales
                document_context = await get_document_context(new_message.content)
                
                # Preparar contexto adicional para consultas de indicadores
                additional_context = ""
                if is_indicator_query:
                    additional_context = "\n\nCONTEXTO ADICIONAL SOBRE INDICADORES:\n" + \
                        "- El promedio general de avance del Plan de Desarrollo es del 25.0%\n" + \
                        "- Se basa en más de 400 indicadores de 16 dependencias principales\n" + \
                        "- Los porcentajes mostrados son PROMEDIOS de avance por dependencia\n" + \
                        "- Dependencias con mejor desempeño: TIC (48.8%), Indersantander (43.65%), Planeación (43.02%)\n" + \
                        "- Marco: Plan 'Es Tiempo de Santander 2024-2027' con 3 ejes estratégicos"
                
                if document_context or additional_context:
                    # Agregar contexto como mensaje del sistema
                    full_context = f"CONTEXTO DE DOCUMENTOS OFICIALES:\n{document_context}{additional_context}\n\n⚠️ INSTRUCCIÓN CRÍTICA: USA EXCLUSIVAMENTE ESTA INFORMACIÓN. CITA FUENTE EXACTA (documento, página) para CADA cifra o dato. Si no encuentras la cifra exacta aquí, NO la inventes. Di 'No dispongo de esa cifra específica'."
                    context_message = llm.ChatMessage.create(
                        text=full_context,
                        role="system"
                    )
                    chat_ctx.items.append(context_message)
                    
                logger.info(f"Contexto agregado para: {new_message.content[:100]}...")
                
            except Exception as e:
                logger.error(f"Error buscando contexto: {e}")
        
        await self.update_chat_ctx(chat_ctx)

async def entrypoint(ctx: JobContext):
    try:
        logger.info(f"Conectando rápidamente a la sala {ctx.room.name}")
        # Reducir timeout para conexión más rápida
        await asyncio.wait_for(ctx.connect(), timeout=10.0)

        logger.info("Inicializando sesión del agente...")

        # 1) Crear modelo LLM con configuración optimizada
        model = openai.realtime.RealtimeModel(
            voice="ash",
            model="gpt-4o-realtime-preview",
            temperature=0.4,  # Reducir temperatura para más precisión
        )

        # 2) Pre-cargar VAD para acelerar inicialización
        logger.info("Cargando VAD...")
        vad = silero.VAD.load()
        
        # 3) Crear sesión con componentes pre-cargados
        session = AgentSession(
            llm=model,
            vad=vad,
        )

        # 4) Crear e iniciar agente
        logger.info("Iniciando agente...")
        agent = GovLabAssistant()
        await session.start(
            room=ctx.room,
            agent=agent,
        )

        # 5) Generar saludo inicial exacto
        await session.generate_reply(
            instructions="Di exactamente este texto sin cambios ni adiciones: '¡Hola! Soy Gober, el asistente virtual de Santander Territorio inteligente. Puedes preguntarme sobre los objetivos estratégicos y avances del departamento. ¿En qué puedo ayudarte hoy?'"
        )

        logger.info("Agente conectado y listo para usar")

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



