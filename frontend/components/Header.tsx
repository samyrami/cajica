import React from 'react';
import Image from 'next/image';

interface HeaderProps {
  className?: string;
}

const Header: React.FC<HeaderProps> = ({ className = '' }) => {
  return (
    <header className={`w-full bg-background border-b border-border py-6 ${className}`}>
      <div className="container mx-auto px-4">
        <div className="flex items-center justify-center gap-8 md:gap-12 lg:gap-16">
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
          
          {/* Gobernación de Santander */}
          <div className="flex items-center justify-center">
            <Image
              src="/images/logo-gobernacion-santander.png"
              alt="Gobernación de Santander"
              width={80}
              height={80}
              className="h-12 md:h-16 w-auto object-contain"
              priority
            />
          </div>
        </div>
        
        <div className="text-center mt-4">
          <h1 className="text-xl md:text-2xl lg:text-3xl font-semibold text-foreground font-institutional">
            Asistente Virtual de la Gobernación de Santander
          </h1>
          <p className="text-muted-foreground mt-2 text-sm md:text-base">
            Consulta transparente sobre objetivos estratégicos y avances institucionales
          </p>
        </div>
      </div>
    </header>
  );
};

export default Header;
