# WARP.md

This file provides guidance to WARP (warp.dev) when working with code in this repository.

## Project Overview

**Gober** is a conversational AI assistant developed by GovLab for Santander Territorio inteligente. It's a full-stack application with a Python backend using LiveKit Agents and a Next.js frontend. The system combines real-time voice interaction capabilities with vector database search for accessing official government documents.

## Architecture

### High-Level Structure
```
Santander_adptado/
├── backend/          # Python LiveKit agent with vector database
├── frontend/         # Next.js React application  
└── README.md         # Project documentation
```

### Backend Architecture (Python)
- **LiveKit Agents**: Real-time conversational AI framework
- **OpenAI Realtime API**: Voice and chat processing
- **ChromaDB Vector Database**: Semantic search of official documents
- **Multi-modal Processing**: PDF and Excel document ingestion

Key modules:
- `agent.py` - Main LiveKit agent with Santander-specific instructions
- `vector_db.py` - Vector database manager (ChromaDB integration)
- `santander_knowledge.py` - Knowledge management and search interface
- `init_database.py` - Database initialization and maintenance

### Frontend Architecture (Next.js)
- **Next.js 14** with App Router
- **LiveKit Components React** for real-time communication
- **Tailwind CSS** with Radix UI components
- **Framer Motion** for animations
- **TypeScript** throughout

Key components:
- `ConversationalAgent.tsx` - Main voice interface component
- `ConversationHistory.tsx` - Chat history management
- `StatsSection.tsx` - Performance metrics display

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

# Initialize vector database (one-time setup)
python init_database.py --clear --stats --test

# Optimize agent performance (recommended before first run)
python optimize_agent.py

# Start the agent
python agent.py dev

# Database management
python init_database.py --stats                    # View database statistics
python init_database.py --clear                   # Clear and reload database
python init_database.py --test                    # Run search tests
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

### Vector Database System
The application uses a sophisticated vector database system for government document search:

- **Document Processing**: Automatic PDF and Excel processing into semantic chunks
- **Multilingual Embeddings**: Uses `paraphrase-multilingual-MiniLM-L12-v2` optimized for Spanish
- **Contextual Metadata**: Each chunk includes source, page, document type, and timestamp
- **Automatic Integration**: Agent automatically searches for relevant context on each user query

### Document Types Classification
- `informe_gestion` - Management reports (main PDD documents)
- `informe_ejecutivo` - Executive summaries  
- `tablero_control` - Control dashboards and indicators
- `datos_complementarios` - Complementary Excel data
- `documento_general` - General documents

### Agent Behavior
The LiveKit agent has specific instructions for Santander Government context:
- Responds as "Gober" - the official Santander Territorio inteligente assistant
- Focuses on transparency and official document citations
- Provides information about the "Es Tiempo de Santander 2024-2027" development plan
- Automatically searches vector database for relevant context on each query

## Testing and Debugging

### Backend Testing
```bash
# Test vector database integration
python init_database.py --test

# View database statistics
python init_database.py --stats

# Check agent logs (run agent in dev mode)
python agent.py dev
```

### Frontend Testing
The frontend integrates with LiveKit's testing infrastructure. Use LiveKit Sandbox for testing:
- Access at https://cloud.livekit.io/projects/p_/sandbox
- Connect your local agent for end-to-end testing

### Performance Optimization
```bash
# Run optimization script before starting agent (recommended)
cd backend
python optimize_agent.py
```

### Common Debug Patterns
- **Slow Connection**: Run `optimize_agent.py` to pre-load database and check performance
- **Vector DB Issues**: Check `chroma_db/` directory exists and contains data
- **LiveKit Connection**: Verify environment variables match between frontend/backend
- **Document Processing**: Check `data/` directory contains PDF/Excel files
- **Agent Responses**: Monitor console logs for vector search results
- **Inaccurate Data**: Agent now requires exact citations - will say "No tengo esa cifra específica" if unsure

## Adding New Documents

To add new government documents to the knowledge base:

1. Place PDF or Excel files in `backend/data/`
2. Run database reinitialization:
   ```bash
   cd backend
   python init_database.py --clear --stats
   ```
3. Test new content:
   ```bash
   python init_database.py --test
   ```

## Performance Considerations

### Vector Database
- ChromaDB runs locally with persistent storage
- Embedding generation happens once during document ingestion
- Search queries typically complete in <2 seconds
- Database supports hundreds of documents without performance issues

### LiveKit Integration
- Uses WebRTC for low-latency voice communication
- Includes Krisp noise filtering for voice quality
- Supports real-time streaming between agent and frontend

## Santander Government Context

This application is specifically designed for the Santander Government (Colombia) and includes:

- Spanish language optimization throughout
- Government transparency compliance (Ley 1712 de 2014)
- Specific knowledge about "Plan de Desarrollo Es Tiempo de Santander 2024-2027"
- Integration with SIGID (Sistema Integrado de Gestión de Información Departamental)
- Three strategic axes: Security, Sustainability, and Prosperity
- 17 sectors, 98 result goals, 106 strategic projects, 375 product goals

When working with the codebase, maintain this government context and ensure all responses cite official sources with exact document references.
