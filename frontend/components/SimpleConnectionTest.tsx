import { useState } from 'react';
import { Card, CardContent } from '@/components/ui/card';

export default function SimpleConnectionTest() {
  const [isConnecting, setIsConnecting] = useState(false);
  const [connectionResult, setConnectionResult] = useState<string>('');

  const testConnection = async () => {
    setIsConnecting(true);
    setConnectionResult('');
    
    try {
      console.log('🔍 Testing basic connection to LiveKit endpoint...');
      
      const response = await fetch('/api/connection-details');
      const data = await response.json();
      
      console.log('✅ Connection details received:', data);
      
      setConnectionResult(`✅ Conexión exitosa!
Server: ${data.serverUrl}
Room: ${data.roomName}
Participant: ${data.participantName}
Token: ${data.participantToken ? 'Presente' : 'Ausente'}`);
      
    } catch (error) {
      console.error('❌ Connection failed:', error);
      setConnectionResult(`❌ Error: ${error instanceof Error ? error.message : 'Unknown error'}`);
    } finally {
      setIsConnecting(false);
    }
  };

  return (
    <Card className="max-w-2xl mx-auto border-primary/20">
      <CardContent className="p-6">
        <h3 className="text-lg font-semibold mb-4 text-center">
          🔧 Prueba de Conexión LiveKit
        </h3>
        
        <div className="text-center space-y-4">
          <button
            onClick={testConnection}
            disabled={isConnecting}
            className="px-6 py-2 bg-primary text-primary-foreground rounded-lg hover:bg-primary/90 disabled:opacity-50"
          >
            {isConnecting ? 'Probando...' : 'Probar Conexión'}
          </button>
          
          {connectionResult && (
            <pre className="text-sm bg-muted p-4 rounded whitespace-pre-wrap text-left">
              {connectionResult}
            </pre>
          )}
        </div>
      </CardContent>
    </Card>
  );
}
