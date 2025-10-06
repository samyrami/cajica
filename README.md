# Asistente Virtual de la Alcaldía de Cajicá



## Descripción
Asistente de IA conversacional desarrollado para la Alcaldía de Cajicá, diseñado específicamente para brindar información sobre el Plan de Desarrollo Municipal 2024-2027 "Cajicá Avanza con Todos". Utiliza tecnologías avanzadas de procesamiento de lenguaje natural y análisis de voz para proporcionar asistencia inteligente a los ciudadanos sobre los objetivos estratégicos, avances e indicadores del municipio.

## Características Principales
- 🎯 Interacción por voz en tiempo real sobre el Plan de Desarrollo de Cajicá
- 📄 Información actualizada de los 18 sectores estratégicos
- 🏆 Consultas sobre avances e indicadores municipales
- 🤝 Interfaz intuitiva para ciudadanos y funcionarios
- 🔒 Seguridad y privacidad de datos
- 🌐 Optimizado para el contexto municipal de Cajicá

## Tecnologías Utilizadas
- OpenAI Realtime API
- WebRTC a través de LiveKit
- React.js
- Framer Motion para animaciones
- Krisp para reducción de ruido
- WebSocket para comunicación en tiempo real

## Requisitos del Sistema
- Node.js 18+
- NPM o Yarn
- Conexión a internet estable
- Micrófono (para funcionalidades de voz)
- API Key de OpenAI

## Instalación

```bash
# Clonar el repositorio
git clone https://github.com/govlab/cajica-assistant.git

# Instalar dependencias
cd cajica-assistant
npm install

# Configurar variables de entorno
cp .env.example .env
# Editar .env con tus credenciales

# Iniciar el servidor de desarrollo
npm run dev
```

## Configuración
Crear un archivo `.env` con las siguientes variables:

```env
OPENAI_API_KEY=tu_api_key
NEXT_PUBLIC_CONN_DETAILS_ENDPOINT=/api/connection-details
```

## Uso
El asistente puede ser utilizado para:

1. **Consultas sobre el Plan de Desarrollo Municipal**
   - Objetivos estratégicos de "Cajicá Avanza con Todos"
   - Avances en las 7 dimensiones estratégicas
   - Indicadores de los 18 sectores municipales

2. **Información Institucional**
   - Estructura organizacional de la Alcaldía
   - Programas y proyectos en ejecución
   - Contacto con dependencias municipales

3. **Servicios al Ciudadano**
   - Trámites y servicios disponibles
   - Información sobre políticas públicas locales
   - Participación ciudadana y rendición de cuentas

## Arquitectura del Sistema

```
cajica-assistant/
├── frontend/
│   ├── app/
│   ├── components/
│   ├── lib/
│   └── public/
├── backend/
│   ├── agent.py
│   └── requirements.txt
└── config/
```

## Seguridad
- Autenticación segura mediante tokens
- Encriptación de datos en tránsito
- Cumplimiento con estándares gubernamentales
- Auditoría de interacciones

## Casos de Uso en Cajicá
- **Consultas Plan de Desarrollo**: Información sobre objetivos estratégicos y avances
- **Indicadores Municipales**: Seguimiento a los 18 sectores del plan municipal
- **Atención al Ciudadano**: Respuestas instantáneas sobre servicios y trámites
- **Transparencia**: Información sobre gestión y rendición de cuentas

## Contribuir
1. Fork del repositorio
2. Crear rama para feature (`git checkout -b feature/AmazingFeature`)
3. Commit cambios (`git commit -m 'Add AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abrir Pull Request

## Soporte
Para soporte técnico o consultas:
- Alcaldía de Cajicá: www.cajica-cundinamarca.gov.co
- Teléfono: (+57) 1 878 2828
- Email: contacto@cajica-cundinamarca.gov.co
- Soporte técnico: soporte@govlab.com

## Licencia
Este proyecto está licenciado bajo términos específicos para uso gubernamental. Contactar a GovLab para más detalles.

## Acerca de GovLab
GovLab es un laboratorio de innovación dedicado a encontrar soluciones a problemas públicos y fortalecer los procesos de toma de decisiones de política pública, utilizando técnicas avanzadas de análisis de datos, co-creación y colaboración intersectorial.

---
Desarrollado con ❤️ por GovLab - Transformando la gestión pública a través de la innovación