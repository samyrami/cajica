"use client";

import { useEffect, useCallback, useState } from 'react';
import { useRoomContext } from '@livekit/components-react';
import { RoomEvent, DataPacket_Kind } from 'livekit-client';

interface ConversationCaptureOptions {
  onUserMessage?: (message: string) => void;
  onAssistantMessage?: (message: string) => void;
  onError?: (error: Error) => void;
}

export function useConversationCapture({
  onUserMessage,
  onAssistantMessage,
  onError
}: ConversationCaptureOptions) {
  const room = useRoomContext();
  const [isCapturing, setIsCapturing] = useState(false);
  const [lastProcessedMessage, setLastProcessedMessage] = useState<string>('');

  // Función para procesar mensajes únicos
  const processUniqueMessage = useCallback((message: string, isUser: boolean) => {
    const trimmedMessage = message.trim();
    
    // Evitar duplicados
    if (trimmedMessage === lastProcessedMessage || !trimmedMessage) {
      return;
    }

    console.log(`Processing ${isUser ? 'user' : 'assistant'} message:`, trimmedMessage);
    setLastProcessedMessage(trimmedMessage);

    if (isUser && onUserMessage) {
      onUserMessage(trimmedMessage);
    } else if (!isUser && onAssistantMessage) {
      onAssistantMessage(trimmedMessage);
    }
  }, [lastProcessedMessage, onUserMessage, onAssistantMessage]);

  useEffect(() => {
    if (!room) {
      setIsCapturing(false);
      return;
    }

    setIsCapturing(true);
    console.log('Starting conversation capture...');

    // Capturar transcripciones nativas de LiveKit
    const handleTranscription = (segments: any[], participant: any, publication: any) => {
      try {
        console.log('Transcription event:', { 
          segments, 
          participantIdentity: participant?.identity,
          localParticipantIdentity: room.localParticipant?.identity
        });

        if (!segments || segments.length === 0) return;

        const text = segments
          .map(segment => segment.text || '')
          .join(' ')
          .trim();

        if (!text) return;

        const isFromUser = participant?.identity === room.localParticipant?.identity;
        processUniqueMessage(text, isFromUser);
        
      } catch (error) {
        console.error('Error processing transcription:', error);
        onError?.(error as Error);
      }
    };

    // Capturar datos del canal de datos
    const handleDataPacket = (payload: Uint8Array, participant: any, kind: DataPacket_Kind) => {
      if (kind !== DataPacket_Kind.RELIABLE) return;

      try {
        const decoder = new TextDecoder();
        const message = decoder.decode(payload);
        const data = JSON.parse(message);

        console.log('Data packet received:', data);

        let text = '';
        let isFromUser = false;

        // Diferentes formatos de datos que puede enviar el agente
        if (data.type === 'transcript' && data.text) {
          text = data.text;
          isFromUser = data.participant_identity === room.localParticipant?.identity;
        } else if (data.type === 'user_transcript' && data.text) {
          text = data.text;
          isFromUser = true;
        } else if (data.type === 'assistant_response' && data.text) {
          text = data.text;
          isFromUser = false;
        } else if (data.type === 'agent_speech' && data.text) {
          text = data.text;
          isFromUser = false;
        } else if (data.text && typeof data.text === 'string') {
          // Formato genérico con texto
          text = data.text;
          isFromUser = participant?.identity === room.localParticipant?.identity;
        }

        if (text) {
          processUniqueMessage(text, isFromUser);
        }

      } catch (error) {
        console.error('Error processing data packet:', error);
        onError?.(error as Error);
      }
    };

    // Registrar event listeners
    room.on(RoomEvent.TranscriptionReceived, handleTranscription);
    room.on(RoomEvent.DataReceived, handleDataPacket);

    // Cleanup
    return () => {
      console.log('Stopping conversation capture...');
      room.off(RoomEvent.TranscriptionReceived, handleTranscription);
      room.off(RoomEvent.DataReceived, handleDataPacket);
      setIsCapturing(false);
    };

  }, [room, processUniqueMessage, onError]);

  return {
    isCapturing,
    room
  };
}
