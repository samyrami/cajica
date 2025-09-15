"use client";

import React, { useState } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { ScrollArea } from '@/components/ui/scroll-area';
import { Button } from '@/components/ui/button';
import { MessageCircle, User, Bot, Trash2, ChevronDown, ChevronUp, Clock } from 'lucide-react';
import { AnimatePresence, motion } from 'framer-motion';

export interface ConversationMessage {
  id: string;
  type: 'user' | 'assistant';
  content: string;
  timestamp: Date;
}

interface ConversationHistoryProps {
  messages: ConversationMessage[];
  onClearHistory: () => void;
  className?: string;
}

const ConversationHistory: React.FC<ConversationHistoryProps> = ({ 
  messages, 
  onClearHistory, 
  className = "" 
}) => {
  const [isExpanded, setIsExpanded] = useState(false);
  const [showTimestamps, setShowTimestamps] = useState(false);

  const formatTime = (date: Date) => {
    return date.toLocaleTimeString('es-CO', { 
      hour: '2-digit', 
      minute: '2-digit',
      second: '2-digit'
    });
  };

  const formatDate = (date: Date) => {
    return date.toLocaleDateString('es-CO', {
      day: 'numeric',
      month: 'short',
      year: 'numeric'
    });
  };

  // Agrupar mensajes por fecha
  const groupedMessages = messages.reduce((acc, message) => {
    const dateKey = message.timestamp.toDateString();
    if (!acc[dateKey]) {
      acc[dateKey] = [];
    }
    acc[dateKey].push(message);
    return acc;
  }, {} as Record<string, ConversationMessage[]>);

  if (messages.length === 0) {
    return (
      <section className={`w-full py-6 ${className}`}>
        <div className="container mx-auto px-4">
          <Card className="max-w-4xl mx-auto border-muted-foreground/20 bg-muted/30">
            <CardContent className="p-8">
              <div className="text-center">
                <MessageCircle className="h-12 w-12 text-muted-foreground mx-auto mb-4 opacity-50" />
                <h3 className="font-semibold text-foreground font-institutional mb-2">
                  Historial de Conversaciones
                </h3>
                <p className="text-sm text-muted-foreground">
                  Aquí aparecerán tus consultas y las respuestas del asistente virtual.
                  ¡Inicia una conversación para comenzar!
                </p>
              </div>
            </CardContent>
          </Card>
        </div>
      </section>
    );
  }

  return (
    <section className={`w-full py-6 ${className}`}>
      <div className="container mx-auto px-4">
        <Card className="max-w-4xl mx-auto border-primary/20 bg-gradient-to-br from-primary/5 to-accent/5">
          <CardHeader className="pb-4">
            <div className="flex items-center justify-between">
              <div className="flex items-center space-x-3">
                <MessageCircle className="h-6 w-6 text-primary" />
                <CardTitle className="text-lg font-institutional text-foreground">
                  Historial de Conversaciones
                </CardTitle>
                <span className="bg-primary/10 text-primary text-xs font-medium px-2 py-1 rounded-full">
                  {messages.length} mensaje{messages.length !== 1 ? 's' : ''}
                </span>
              </div>
              
              <div className="flex items-center space-x-2">
                <Button
                  variant="ghost"
                  size="sm"
                  onClick={() => setShowTimestamps(!showTimestamps)}
                  className="h-8 w-8 p-0"
                >
                  <Clock className="h-4 w-4" />
                </Button>
                
                {isExpanded ? (
                  <Button
                    variant="ghost"
                    size="sm"
                    onClick={() => setIsExpanded(false)}
                    className="h-8 w-8 p-0"
                  >
                    <ChevronUp className="h-4 w-4" />
                  </Button>
                ) : (
                  <Button
                    variant="ghost"
                    size="sm"
                    onClick={() => setIsExpanded(true)}
                    className="h-8 w-8 p-0"
                  >
                    <ChevronDown className="h-4 w-4" />
                  </Button>
                )}
                
                <Button
                  variant="ghost"
                  size="sm"
                  onClick={onClearHistory}
                  className="h-8 w-8 p-0 text-destructive hover:text-destructive"
                >
                  <Trash2 className="h-4 w-4" />
                </Button>
              </div>
            </div>
          </CardHeader>
          
          <CardContent className="pt-0">
            <AnimatePresence>
              {isExpanded && (
                <motion.div
                  initial={{ opacity: 0, height: 0 }}
                  animate={{ opacity: 1, height: 'auto' }}
                  exit={{ opacity: 0, height: 0 }}
                  transition={{ duration: 0.3 }}
                >
                  <ScrollArea className="h-80 w-full pr-4">
                    <div className="space-y-4">
                      {Object.entries(groupedMessages)
                        .sort(([a], [b]) => new Date(b).getTime() - new Date(a).getTime())
                        .map(([dateKey, dayMessages]) => (
                          <div key={dateKey} className="space-y-3">
                            <div className="text-center">
                              <span className="text-xs text-muted-foreground bg-muted px-2 py-1 rounded-full">
                                {formatDate(new Date(dateKey))}
                              </span>
                            </div>
                            
                            {dayMessages
                              .sort((a, b) => b.timestamp.getTime() - a.timestamp.getTime())
                              .map((message) => (
                                <motion.div
                                  key={message.id}
                                  initial={{ opacity: 0, x: message.type === 'user' ? 20 : -20 }}
                                  animate={{ opacity: 1, x: 0 }}
                                  transition={{ duration: 0.3, ease: 'easeOut' }}
                                  className={`conversation-message flex items-start space-x-3 ${
                                    message.type === 'user' ? 'flex-row-reverse space-x-reverse' : ''
                                  }`}
                                >
                                  <div className={`
                                    flex-shrink-0 w-8 h-8 rounded-full flex items-center justify-center
                                    ${message.type === 'user' 
                                      ? 'bg-secondary text-secondary-foreground' 
                                      : 'bg-primary text-primary-foreground'
                                    }
                                  `}>
                                    {message.type === 'user' ? (
                                      <User className="h-4 w-4" />
                                    ) : (
                                      <Bot className="h-4 w-4" />
                                    )}
                                  </div>
                                  
                                  <div className={`
                                    flex-1 max-w-[75%] space-y-1
                                    ${message.type === 'user' ? 'text-right' : 'text-left'}
                                  `}>
                                    <div className={`
                                      inline-block px-4 py-2 rounded-lg text-sm leading-relaxed
                                      ${message.type === 'user'
                                        ? 'bg-secondary text-secondary-foreground rounded-br-sm'
                                        : 'bg-muted text-foreground rounded-bl-sm'
                                      }
                                    `}>
                                      {message.content}
                                    </div>
                                    
                                    {showTimestamps && (
                                      <div className="text-xs text-muted-foreground">
                                        {formatTime(message.timestamp)}
                                      </div>
                                    )}
                                  </div>
                                </motion.div>
                              ))}
                          </div>
                        ))}
                    </div>
                  </ScrollArea>
                </motion.div>
              )}
            </AnimatePresence>
            
            {!isExpanded && messages.length > 0 && (
              <div className="text-center py-4">
                <p className="text-sm text-muted-foreground mb-3">
                  Última conversación hace {Math.floor((Date.now() - messages[messages.length - 1].timestamp.getTime()) / (1000 * 60))} minutos
                </p>
                <div className="text-xs text-muted-foreground mb-3 bg-muted/50 px-3 py-2 rounded-lg max-w-md mx-auto">
                  <div className="flex items-center justify-center space-x-2">
                    {messages.slice(-1).map(msg => (
                      <div key={msg.id} className="flex items-center space-x-2">
                        {msg.type === 'user' ? (
                          <User className="h-3 w-3 text-secondary" />
                        ) : (
                          <Bot className="h-3 w-3 text-primary" />
                        )}
                        <span className="truncate max-w-[200px]">
                          {msg.content.length > 50 ? `${msg.content.slice(0, 50)}...` : msg.content}
                        </span>
                      </div>
                    ))}
                  </div>
                </div>
                <Button
                  variant="outline"
                  size="sm"
                  onClick={() => setIsExpanded(true)}
                  className="text-primary border-primary/20 hover:bg-primary/10 transition-colors duration-200"
                >
                  Ver conversaciones completas
                  <ChevronDown className="h-4 w-4 ml-2" />
                </Button>
              </div>
            )}
          </CardContent>
        </Card>
      </div>
    </section>
  );
};

export default ConversationHistory;
