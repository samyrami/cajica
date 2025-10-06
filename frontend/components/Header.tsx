import React from 'react';
import Image from 'next/image';

interface HeaderProps {
  className?: string;
}

const Header: React.FC<HeaderProps> = ({ className = '' }) => {
  return (
    <header className={`w-full bg-white border-b border-border py-6 ${className}`}>
      <div className="container mx-auto px-4">
        <div className="flex items-center justify-center gap-8 md:gap-12 lg:gap-16">
          {/* Escudo de Cajicá */}
          <div className="flex items-center justify-center">
            <Image
              src="/images/Escudo_de_Cajicá.svg"
              alt="Escudo de Cajicá"
              width={80}
              height={80}
              className="h-12 md:h-16 w-auto object-contain bg-white rounded-lg p-2 shadow-lg"
              priority
            />
          </div>
          
          {/* Universidad de La Sabana */}
          <div className="flex items-center justify-center">
            <Image
              src="/images/logo-unisabana.png"
              alt="Universidad de La Sabana"
              width={80}
              height={80}
              className="h-12 md:h-16 w-auto object-contain"
              priority
            />
          </div>
          
          {/* Laboratorio de Gobierno */}
          <div className="flex items-center justify-center">
            <Image
              src="/images/logo-laboratorio-gobierno.png"
              alt="Laboratorio de Gobierno"
              width={80}
              height={80}
              className="h-12 md:h-16 w-auto object-contain"
              priority
            />
          </div>
        </div>
        
        <div className="text-center mt-4">
          <h1 className="text-xl md:text-2xl lg:text-3xl font-semibold text-gray-800 font-institutional">
            Asistente Virtual - Alcaldía de Cajicá
          </h1>
          <p className="text-gray-600 mt-2 text-sm md:text-base">
            Plan de Desarrollo &ldquo;Cajicá Ideal 2024-2027&rdquo; - Consulta transparente e indicadores municipales
          </p>
        </div>
      </div>
    </header>
  );
};

export default Header;
