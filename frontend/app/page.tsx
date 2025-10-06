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
                    Asistente Virtual Oficial de Cajicá
                  </h3>
                  <p className="text-sm text-muted-foreground leading-relaxed">
                    Este asistente de voz proporciona información verificada y actualizada sobre el Plan de Desarrollo 
                    Municipal "Cajicá Ideal 2024-2027". Desarrollado en colaboración con la Universidad de La Sabana 
                    y el Laboratorio de Gobierno para promover la transparencia municipal y el acceso ciudadano 
                    a la información pública.
                  </p>
                </div>
              </div>
            </CardContent>
          </Card>
        </section>

        {/* Placeholder de la Alcaldesa */}
        <section className="py-6 bg-white">
          <div className="flex justify-center">
            {/* Placeholder Elegante de la Alcaldesa */}
            <div className="relative group">
              {/* Círculo de fondo con efecto sutil */}
              <div className="absolute inset-0 w-32 h-32 md:w-40 md:h-40 rounded-full bg-gradient-to-r from-cajica-green/10 to-cajica-gold/10 blur-sm group-hover:blur-md transition-all duration-300"></div>
              <div className="relative w-32 h-32 md:w-40 md:h-40 rounded-full border-2 border-gray-200 shadow-lg bg-white group-hover:scale-105 transition-transform duration-300 overflow-hidden">
                {/* Imagen real de la alcaldesa */}
                <Image
                  src="/images/alcaldesa.png"
                  alt="Fabiola Jácome Rincón - Alcaldesa de Cajicá"
                  width={160}
                  height={160}
                  className="w-full h-full object-cover"
                  priority
                />
              </div>
              {/* Etiqueta de la Alcaldesa */}
              <div className="absolute -bottom-8 left-1/2 transform -translate-x-1/2">
                <p className="text-xs md:text-sm text-muted-foreground text-center whitespace-nowrap">
                  Fabiola Jácome Rincón
                </p>
                <p className="text-xs text-muted-foreground/70 text-center">
                  Alcaldesa de Cajicá
                </p>
              </div>
            </div>
          </div>
        </section>

        {/* Interfaz de voz principal */}
        <section className="py-12">
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
                  <li>• Plan de Desarrollo "Cajicá Ideal 2024-2027"</li>
                  <li>• Indicadores por dimensiones estratégicas</li>
                  <li>• Servicios municipales y coberturas</li>
                  <li>• Programas sociales, culturales y deportivos</li>
                  <li>• Proyectos ambientales y de sostenibilidad</li>
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
                      La información proporcionada es oficial y verificada por la Alcaldía de Cajicá. 
                      Para consultas específicas o trámites administrativos, contacte directamente las oficinas 
                      municipales correspondientes o visite la página oficial del municipio.
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
            © 2024 Alcaldía de Cajicá - Universidad de La Sabana - Laboratorio de Gobierno
          </p>
          <p className="text-xs text-muted-foreground mt-1">
            Comprometidos con la transparencia municipal y la modernización del servicio público
          </p>
        </div>
      </footer>
    </div>
  );
}
