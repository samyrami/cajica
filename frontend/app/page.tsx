"use client";

import React, { useState, useCallback } from 'react';
import Header from '@/components/Header';
import ConversationalAgent from '@/components/ConversationalAgent';
import ConversationHistory, { ConversationMessage } from '@/components/ConversationHistory';
import StatsSection from '@/components/StatsSection';
import { Card, CardContent } from '@/components/ui/card';
import { AlertTriangle, Info } from 'lucide-react';
import Image from 'next/image';

export default function Page() {
  const [currentResponse, setCurrentResponse] = useState<string>('');
  const [conversationHistory, setConversationHistory] = useState<ConversationMessage[]>([]);

  const handleVoiceResponse = (response: string) => {
    setCurrentResponse(response);
  };

  const addMessageToHistory = useCallback((type: 'user' | 'assistant', content: string) => {
    const newMessage: ConversationMessage = {
      id: `${Date.now()}-${Math.random()}`,
      type,
      content,
      timestamp: new Date()
    };
    setConversationHistory(prev => [...prev, newMessage]);
  }, []);

  const clearConversationHistory = useCallback(() => {
    setConversationHistory([]);
  }, []);

  return (
    <div className="min-h-screen bg-background">
      {/* Encabezado con logos institucionales */}
      <Header />

      {/* Contenido principal */}
      <main className="container mx-auto px-4">
        {/* Información institucional */}
        <section className="py-8">
          <Card className="max-w-4xl mx-auto border-primary/20 bg-primary-light/30">
            <CardContent className="p-6">
              <div className="flex items-start space-x-3">
                <Info className="h-6 w-6 text-primary mt-0.5 flex-shrink-0" />
                <div className="space-y-2">
                  <h3 className="font-semibold text-foreground font-institutional">
                    Asistente Virtual Oficial
                  </h3>
                  <p className="text-sm text-muted-foreground leading-relaxed">
                    Este asistente de voz proporciona información verificada y actualizada sobre los objetivos 
                    estratégicos de Santander Territorio inteligente. Desarrollado en colaboración con la Universidad 
                    de La Sabana y el Laboratorio de Gobierno para promover la transparencia y el acceso ciudadano 
                    a la información pública.
                  </p>
                </div>
              </div>
            </CardContent>
          </Card>
        </section>

        {/* Imagen del Gobernador */}
        <section className="py-6">
          <div className="flex justify-center">
            <div className="relative group">
              {/* Círculo de fondo con efecto de resplandor */}
              <div className="absolute inset-0 w-32 h-32 md:w-40 md:h-40 rounded-full bg-gradient-to-r from-primary/30 to-accent/30 blur-md group-hover:blur-lg transition-all duration-300"></div>
              <div className="relative w-32 h-32 md:w-40 md:h-40 rounded-full overflow-hidden border-4 border-white/80 shadow-2xl bg-gradient-to-br from-primary/10 to-accent/10 group-hover:scale-105 transition-transform duration-300">
                <Image
                  src="/images/Gobernado_santander.jpeg"
                  alt="Gobernador de Santander"
                  width={160}
                  height={160}
                  className="w-full h-full object-cover"
                  priority
                  onError={(e) => {
                    // Fallback si no se encuentra la imagen
                    const target = e.target as HTMLImageElement;
                    target.style.display = 'none';
                    const parent = target.parentElement;
                    if (parent) {
                      parent.innerHTML = `
                        <div class="w-full h-full flex items-center justify-center bg-primary/10 text-primary">
                          <svg class="w-16 h-16" fill="currentColor" viewBox="0 0 20 20">
                            <path fill-rule="evenodd" d="M10 9a3 3 0 100-6 3 3 0 000 6zm-7 9a7 7 0 1114 0H3z" clip-rule="evenodd"/>
                          </svg>
                        </div>
                      `;
                    }
                  }}
                />
              </div>
            </div>
          </div>
        </section>

        {/* Interfaz de voz principal */}
        <section className="py-8">
          <ConversationalAgent 
            onResponse={handleVoiceResponse} 
            onAddMessage={addMessageToHistory}
          />
        </section>

        {/* Respuesta actual destacada */}
        {currentResponse && (
          <section className="py-4">
            <Card className="max-w-4xl mx-auto border-secondary/20 bg-secondary-light/30">
              <CardContent className="p-6">
                <h3 className="font-semibold text-foreground font-institutional mb-3">
                  Última Consulta Procesada:
                </h3>
                <p className="text-foreground leading-relaxed">
                  {currentResponse}
                </p>
              </CardContent>
            </Card>
          </section>
        )}

        {/* Historial de conversaciones */}
        <ConversationHistory 
          messages={conversationHistory}
          onClearHistory={clearConversationHistory}
        />

        {/* Estadísticas de objetivos estratégicos */}
        <StatsSection />

        {/* Información adicional */}
        <section className="py-8">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6 max-w-4xl mx-auto">
            <Card>
              <CardContent className="p-6">
                <h3 className="font-semibold text-foreground font-institutional mb-3">
                  Tipos de Consultas Disponibles
                </h3>
                <ul className="space-y-2 text-sm text-muted-foreground">
                  <li>• Avances en desarrollo social y educación</li>
                  <li>• Progreso en infraestructura y conectividad</li>
                  <li>• Iniciativas de gestión ambiental</li>
                  <li>• Proyectos de fortalecimiento institucional</li>
                  <li>• Indicadores de impacto ciudadano</li>
                </ul>
              </CardContent>
            </Card>

            <Card className="border-primary/20">
              <CardContent className="p-6">
                <div className="flex items-start space-x-3">
                  <AlertTriangle className="h-5 w-5 text-primary mt-0.5 flex-shrink-0" />
                  <div>
                    <h3 className="font-semibold text-foreground font-institutional mb-3">
                      Nota Importante
                    </h3>
                    <p className="text-sm text-muted-foreground leading-relaxed">
                      La información proporcionada es oficial y verificada por Santander Territorio inteligente. 
                      Para consultas específicas o trámites administrativos, contacte directamente las oficinas 
                      departamentales correspondientes.
                    </p>
                  </div>
                </div>
              </CardContent>
            </Card>
          </div>
        </section>
      </main>

      {/* Pie de página institucional */}
      <footer className="border-t border-border bg-muted/30 py-6 mt-12">
        <div className="container mx-auto px-4 text-center">
          <p className="text-sm text-muted-foreground">
            © 2024 Santander Territorio inteligente - Universidad de La Sabana - Laboratorio de Gobierno
          </p>
          <p className="text-xs text-muted-foreground mt-1">
            Comprometidos con la transparencia y la modernización del servicio público
          </p>
        </div>
      </footer>
    </div>
  );
}
