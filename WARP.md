# WARP.md

This file provides guidance to WARP (warp.dev) when working with code in this repository.

## Project Overview

**Asistente Virtual de Cajicá** is a conversational AI assistant developed by GovLab for the Alcaldía de Cajicá. It's a full-stack application with a Python backend using LiveKit Agents and a Next.js frontend. The system combines real-time voice interaction capabilities with access to official municipal government information about the Plan de Desarrollo Municipal "Cajicá Ideal 2024-2027".

## Architecture

### High-Level Structure
```
cajica/
├── backend/          # Python LiveKit agent with Cajicá knowledge
├── frontend/         # Next.js React application with Cajicá branding
└── README.md         # Project documentation
```

### Backend Architecture (Python)
- **LiveKit Agents**: Real-time conversational AI framework
- **OpenAI Realtime API**: Voice and chat processing
- **ChromaDB Vector Database**: Semantic search of official documents
- **Multi-modal Processing**: PDF and Excel document ingestion

Key modules:
- `agent.py` - Main LiveKit agent with Cajicá municipal knowledge

### Frontend Architecture (Next.js)
- **Next.js 14** with App Router
- **LiveKit Components React** for real-time communication
- **Tailwind CSS** with Radix UI components
- **Framer Motion** for animations
- **TypeScript** throughout

Key components:
- `ConversationalAgent.tsx` - Main voice interface component
- `ConversationHistory.tsx` - Chat history management
- `StatsSection.tsx` - Municipal metrics and Plan de Desarrollo indicators display
- `Header.tsx` - Municipal branding with Alcaldesa information

## Development Commands

### Backend Development
```bash
# Setup virtual environment
cd backend
python -m venv venv

# Windows
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the Cajicá assistant agent

# Start the agent
python agent.py dev

# The agent now contains embedded knowledge about Cajicá's Plan de Desarrollo
```

### Frontend Development
```bash
cd frontend

# Install dependencies
npm install

# Development server
npm run dev

# Production build
npm run build
npm run start

# Linting
npm run lint
```

### Environment Configuration

#### Backend (.env.local)
Required environment variables in `backend/.env.local`:
```
LIVEKIT_URL=wss://your-livekit-server.com
LIVEKIT_API_KEY=your_api_key
LIVEKIT_API_SECRET=your_api_secret
OPENAI_API_KEY=your_openai_key
```

#### Frontend (.env.local)
Required environment variables in `frontend/.env.local`:
```
NEXT_PUBLIC_LIVEKIT_URL=wss://your-livekit-server.com
LIVEKIT_API_KEY=your_api_key
LIVEKIT_API_SECRET=your_api_secret
NEXT_PUBLIC_CONN_DETAILS_ENDPOINT=/api/connection-details
```

## Key Development Concepts

### Municipal Knowledge System
The application contains comprehensive information about Cajicá's municipal government:

- **Plan de Desarrollo**: Complete information about "Cajicá Ideal 2024-2027"
- **Municipal Indicators**: Data on all 18 sectors and 7 strategic dimensions
- **Local Context**: Population, services, infrastructure, and municipal programs
- **Integrated Response**: Agent provides contextual responses based on official municipal data

### Municipal Information Categories
- **Plan de Desarrollo**: Strategic objectives and sectoral goals
- **Municipal Indicators**: Progress metrics for all 18 sectors
- **Institutional Information**: Alcaldesa biography, municipal structure
- **Public Services**: Coverage data, infrastructure information
- **Municipal Programs**: Cultural, sports, educational, and social programs

### Agent Behavior
The LiveKit agent has specific instructions for Cajicá Municipal context:
- Responds as the official Cajicá Municipal virtual assistant
- Focuses on transparency and citizen service
- Provides information about the "Cajicá Ideal 2024-2027" development plan
- Responds with accurate information based on embedded municipal knowledge

## Testing and Debugging

### Backend Testing
```bash
# Test the Cajicá agent
python agent.py dev

# Agent includes comprehensive Cajicá municipal knowledge
```

### Frontend Testing
The frontend integrates with LiveKit's testing infrastructure. Use LiveKit Sandbox for testing:
- Access at https://cloud.livekit.io/projects/p_/sandbox
- Connect your local agent for end-to-end testing

### Performance Optimization
The agent is optimized with embedded municipal knowledge for fast responses.

### Common Debug Patterns
- **LiveKit Connection**: Verify environment variables match between frontend/backend
- **Agent Responses**: Monitor console logs for response generation
- **Municipal Data**: Agent provides information based on embedded Cajicá knowledge
- **Accuracy**: Agent maintains high accuracy with municipal-specific information

## Municipal Knowledge Updates

The agent contains comprehensive embedded knowledge about Cajicá's municipal government. To update municipal information, modify the agent's instructions in `backend/agent.py` with new official data from the Alcaldía de Cajicá.

## Performance Considerations

### Municipal Knowledge System
- Embedded knowledge provides instant responses
- No database queries required for municipal information
- Responses are based on official municipal data
- Optimized for Spanish language and local context

### LiveKit Integration
- Uses WebRTC for low-latency voice communication
- Includes Krisp noise filtering for voice quality
- Supports real-time streaming between agent and frontend

## Cajicá Municipal Government Context

This application is specifically designed for the Alcaldía de Cajicá (Colombia) and includes:

- Spanish language optimization for Colombian municipal context
- Government transparency compliance (Ley 1712 de 2014)
- Specific knowledge about "Plan de Desarrollo Cajicá Ideal 2024-2027"
- Information about Alcaldesa Fabiola Jácome Rincón and municipal structure
- Five strategic dimensions: Environmental, Social, Productive, Mobility, and Governance
- 18 municipal sectors with specific indicators and goals
- Municipal services, demographics, and infrastructure information

When working with the codebase, maintain this municipal context and ensure all responses provide accurate information about Cajicá's municipal government and Plan de Desarrollo.
