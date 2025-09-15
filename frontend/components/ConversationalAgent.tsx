"use client";

import { AnimatePresence, motion } from "framer-motion";
import {
  LiveKitRoom,
  useVoiceAssistant,
  BarVisualizer,
  RoomAudioRenderer,
  VoiceAssistantControlBar,
  AgentState,
  DisconnectButton,
  useRoomContext,
  useDataChannel,
  useTrackTranscription,
} from "@livekit/components-react";
import { useCallback, useEffect, useState } from "react";
import { MediaDeviceFailure, RoomEvent, DataPacket_Kind, TrackReference } from "livekit-client";
import type { ConnectionDetails } from "../app/api/connection-details/route";
import { NoAgentNotification } from "@/components/NoAgentNotification";
import { CloseIcon } from "@/components/CloseIcon";
// import { useKrispNoiseFilter } from "@livekit/components-react/krisp"; // Comentado temporalmente para evitar bucles
import { Card, CardContent } from "@/components/ui/card";
import { useConversationCapture } from "@/hooks/useConversationCapture";

interface ConversationalAgentProps {
  onResponse?: (response: string) => void;
  onAddMessage?: (type: 'user' | 'assistant', content: string) => void;
}

const ConversationalAgent: React.FC<ConversationalAgentProps> = ({ onResponse, onAddMessage }) => {
  const [connectionDetails, updateConnectionDetails] = useState<
    ConnectionDetails | undefined
  >(undefined);
  const [agentState, setAgentState] = useState<AgentState>("disconnected");
  const [connectionError, setConnectionError] = useState<string | null>(null);

  const onConnectButtonClicked = useCallback(async () => {
    try {
      console.log('Attempting to connect...');
      setConnectionError(null);
      
      const url = new URL(
        process.env.NEXT_PUBLIC_CONN_DETAILS_ENDPOINT ??
        "/api/connection-details",
        window.location.origin
      );
      console.log('Fetching connection details from:', url.toString());
      
      const response = await fetch(url.toString());
      if (!response.ok) {
        throw new Error(`Error del servidor: ${response.status} - ${response.statusText}`);
      }
      
      const connectionDetailsData = await response.json();
      console.log('Connection details received:', connectionDetailsData);
      
      if (!connectionDetailsData.serverUrl || !connectionDetailsData.participantToken) {
        throw new Error('Datos de conexión incompletos recibidos del servidor');
      }
      
      updateConnectionDetails(connectionDetailsData);
    } catch (error) {
      console.error('Error connecting:', error);
      const errorMessage = error instanceof Error ? error.message : 'Error desconocido';
      setConnectionError(`No se pudo conectar: ${errorMessage}. Asegúrate de que el agente esté ejecutándose.`);
    }
  }, []);

  // Usar hook personalizado para capturar conversaciones
  const { isCapturing } = useConversationCapture({
    onUserMessage: useCallback((message: string) => {
      console.log('User message captured:', message);
      setLastUserTranscript(message);
      if (onAddMessage) {
        onAddMessage('user', message);
      }
    }, [onAddMessage]),
    
    onAssistantMessage: useCallback((message: string) => {
      console.log('Assistant message captured:', message);
      if (onResponse) {
        onResponse(message);
      }
      if (onAddMessage) {
        onAddMessage('assistant', message);
      }
    }, [onResponse, onAddMessage]),
    
    onError: useCallback((error: Error) => {
      console.error('Conversation capture error:', error);
    }, [])
  });

  // State para controlar cuándo agregar mensajes al historial
  const [lastProcessedState, setLastProcessedState] = useState<AgentState>("disconnected");
  const [hasAddedWelcomeMessage, setHasAddedWelcomeMessage] = useState(false);
  const [pendingUserMessage, setPendingUserMessage] = useState<string | null>(null);
  const [lastUserTranscript, setLastUserTranscript] = useState<string>('');

  // Solo manejar estado inicial para respuesta genérica si no hay transcripciones
  useEffect(() => {
    if (agentState === "speaking" && !lastUserTranscript && onResponse) {
      onResponse("Procesando su consulta sobre los objetivos estratégicos de la Gobernación de Santander...");
    }
  }, [agentState, onResponse, lastUserTranscript]);

  // Debug logs y mensaje de bienvenida
  useEffect(() => {
    console.log('Agent state changed:', agentState);
  }, [agentState]);

  // Agregar mensaje de bienvenida cuando el agente se conecte exitosamente
  useEffect(() => {
    if (agentState === 'listening' && !hasAddedWelcomeMessage && onAddMessage) {
      console.log('Adding welcome message - agent ready');
      setTimeout(() => {
        onAddMessage('assistant', '¡Hola! Soy Sentir Santander, el asistente virtual de la Gobernación de Santander. Puedes preguntarme sobre los objetivos estratégicos y avances del departamento.');
      }, 1000); // Delay para asegurar que la conexión esté estable
      setHasAddedWelcomeMessage(true);
    }
  }, [agentState, hasAddedWelcomeMessage, onAddMessage]);

  // Manejar transiciones de estado simplificadas
  useEffect(() => {
    if (lastProcessedState !== agentState) {
      console.log('State transition:', lastProcessedState, '->', agentState);
      setLastProcessedState(agentState);
    }
  }, [agentState, lastProcessedState]);

  return (
    <div className="w-full max-w-4xl mx-auto">
      <Card className="border-primary/20 bg-gradient-to-br from-primary/5 to-accent/5">
        <CardContent className="p-8">
          <div className="text-center mb-6">
            <h2 className="text-2xl font-bold text-foreground font-institutional mb-2">
              Sentir Santander
            </h2>
            <p className="text-muted-foreground">
              ¿En qué puedo ayudarte hoy? Puedes hablar conmigo usando el micrófono o escribir tu consulta.
            </p>
            
            {/* Mostrar estado de conexión */}
            <div className="mt-3 text-sm flex items-center justify-center space-x-3">
              <span className={`inline-flex items-center px-2 py-1 rounded-full text-xs font-medium ${
                agentState === 'listening' ? 'bg-green-100 text-green-800' :
                agentState === 'thinking' ? 'bg-yellow-100 text-yellow-800' :
                agentState === 'speaking' ? 'bg-blue-100 text-blue-800' :
                agentState === 'connecting' ? 'bg-orange-100 text-orange-800' :
                'bg-gray-100 text-gray-800'
              }`}>
                {agentState === 'listening' ? '🟢 Escuchando' :
                 agentState === 'thinking' ? '🟡 Procesando' :
                 agentState === 'speaking' ? '🔵 Respondiendo' :
                 agentState === 'connecting' ? '🟠 Conectando...' :
                 '⚫ Desconectado'}
              </span>
              
              {isCapturing && agentState !== 'disconnected' && (
                <span className="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-purple-100 text-purple-800">
                  📁 Guardando conversación
                </span>
              )}
            </div>
            
            {connectionError && (
              <div className="mt-4 p-4 bg-destructive/10 border border-destructive/20 rounded-lg">
                <p className="text-destructive text-sm mb-2">
                  ⚠️ {connectionError}
                </p>
                <div className="text-muted-foreground text-xs space-y-1">
                  <p>Posibles soluciones:</p>
                  <ul className="list-disc list-inside space-y-1 text-left max-w-md mx-auto">
                    <li>Verifica que el backend esté ejecutándose: <code className="bg-muted px-1 rounded">python agent.py dev</code></li>
                    <li>Revisa tu conexión a internet</li>
                    <li>Si estás en una red corporativa, puede haber restricciones de firewall</li>
                    <li><strong>Problema de audio:</strong> Verifica permisos de micrófono en el navegador</li>
                    <li>Abre F12 &gt; Consola para ver errores de audio</li>
                  </ul>
                </div>
              </div>
            )}
          </div>

          <LiveKitRoom
            token={connectionDetails?.participantToken}
            serverUrl={connectionDetails?.serverUrl}
            connect={connectionDetails !== undefined}
            audio={true}
            video={false}
            onMediaDeviceFailure={onDeviceFailure}
            onDisconnected={() => {
              console.log('Room disconnected');
              updateConnectionDetails(undefined);
              setHasAddedWelcomeMessage(false); // Reset para permitir mensaje de bienvenida en nueva conexión
            }}
            onConnected={() => {
              console.log('Room connected successfully');
              setConnectionError(null); // Limpiar errores previos
            }}
            options={{
              adaptiveStream: true,
              dynacast: true,
              publishDefaults: {
                videoSimulcastLayers: []
              },
              // Timeouts más largos y configuraciones de estabilidad
              disconnectOnPageLeave: true,
              stopLocalTrackOnUnpublish: true,
              // Configuraciones para evitar desconexiones
              reconnectPolicy: {
                nextRetryDelayInMs: (context) => {
                  // Incrementar delay progresivamente
                  return Math.min(1000 * Math.pow(2, context.retryCount), 30000);
                }
              }
            }}
            className="flex flex-col items-center space-y-6"
          >
            <SimpleVoiceAssistant 
              onStateChange={setAgentState}
            />
            <ControlBar
              onConnectButtonClicked={onConnectButtonClicked}
              agentState={agentState}
            />
            <RoomAudioRenderer />
            <NoAgentNotification state={agentState} />
          </LiveKitRoom>
        </CardContent>
      </Card>
    </div>
  );
};

function SimpleVoiceAssistant(props: {
  onStateChange: (state: AgentState) => void;
}) {
  const { state, audioTrack } = useVoiceAssistant();
  const { onStateChange } = props;
  
  useEffect(() => {
    onStateChange(state);
  }, [state, onStateChange]);

  return (
    <div className="h-[300px] max-w-[90vw] mx-auto">
      <BarVisualizer
        state={state}
        barCount={5}
        trackRef={audioTrack}
        className="agent-visualizer"
        options={{ minHeight: 24 }}
      />
    </div>
  );
}

function ControlBar(props: {
  onConnectButtonClicked: () => void;
  agentState: AgentState;
}) {
  // Krisp noise filter temporalmente deshabilitado para evitar bucles infinitos
  // TODO: Reactivar cuando se resuelva el problema de bucle infinito

  return (
    <div className="relative h-[60px] w-full flex items-center justify-center">
      <AnimatePresence>
        {props.agentState === "disconnected" && (
          <motion.button
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -10 }}
            transition={{ duration: 0.3, ease: "easeOut" }}
            className="px-8 py-3 bg-primary text-primary-foreground rounded-lg font-medium hover:bg-primary/90 transition-colors duration-200 shadow-lg hover:shadow-xl"
            onClick={() => props.onConnectButtonClicked()}
          >
            🎙️ Haz clic aquí y pregúntame sobre la Gobernación de Santander
          </motion.button>
        )}
      </AnimatePresence>
      
      <AnimatePresence>
        {props.agentState !== "disconnected" &&
          props.agentState !== "connecting" && (
            <motion.div
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -10 }}
              transition={{ duration: 0.2, ease: "easeOut" }}
              className="flex items-center justify-center space-x-3"
            >
              <VoiceAssistantControlBar controls={{ leave: false }} />
              <DisconnectButton>
                <CloseIcon />
              </DisconnectButton>
            </motion.div>
          )}
      </AnimatePresence>
    </div>
  );
}

function onDeviceFailure(error?: MediaDeviceFailure) {
  console.error(error);
  alert(
    "Error adquiriendo permisos de cámara o micrófono. Por favor asegúrate de conceder los permisos necesarios en tu navegador y recarga la pestaña"
  );
}

export default ConversationalAgent;
