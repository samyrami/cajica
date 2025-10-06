import React, { useState } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Progress } from '@/components/ui/progress';
import { Users, Building2, Leaf, Shield, GraduationCap, Heart, Home, Wrench, ChevronDown, ChevronUp } from 'lucide-react';

interface DepartmentData {
  name: string;
  averageProgress: number;
  totalIndicators: number;
  completedIndicators: number;
  icon: React.ReactNode;
  color: 'primary' | 'secondary' | 'accent' | 'blue';
}

const departmentData: DepartmentData[] = [
  {
    name: "Ambiente y Desarrollo Sostenible",
    averageProgress: 95.5,
    totalIndicators: 8,
    completedIndicators: 7,
    icon: <Leaf className="h-5 w-5" />,
    color: 'primary'
  },
  {
    name: "Educación",
    averageProgress: 82.1,
    totalIndicators: 6,
    completedIndicators: 4,
    icon: <GraduationCap className="h-5 w-5" />,
    color: 'secondary'
  },
  {
    name: "Salud y Protección Social",
    averageProgress: 76.3,
    totalIndicators: 7,
    completedIndicators: 5,
    icon: <Heart className="h-5 w-5" />,
    color: 'accent'
  },
  {
    name: "Cultura",
    averageProgress: 74.8,
    totalIndicators: 12,
    completedIndicators: 8,
    icon: <Building2 className="h-5 w-5" />,
    color: 'primary'
  },
  {
    name: "Deporte y Recreación",
    averageProgress: 68.9,
    totalIndicators: 9,
    completedIndicators: 6,
    icon: <Users className="h-5 w-5" />,
    color: 'secondary'
  },
  {
    name: "Tecnologías de la Información (TIC)",
    averageProgress: 65.2,
    totalIndicators: 4,
    completedIndicators: 2,
    icon: <Building2 className="h-5 w-5" />,
    color: 'accent'
  },
  {
    name: "Comercio, Industria y Turismo",
    averageProgress: 58.7,
    totalIndicators: 15,
    completedIndicators: 9,
    icon: <Building2 className="h-5 w-5" />,
    color: 'primary'
  },
  {
    name: "Ciencia, Tecnología e Innovación",
    averageProgress: 52.4,
    totalIndicators: 4,
    completedIndicators: 2,
    icon: <Building2 className="h-5 w-5" />,
    color: 'secondary'
  },
  {
    name: "Inclusión Social y Reconciliación",
    averageProgress: 48.6,
    totalIndicators: 8,
    completedIndicators: 3,
    icon: <Users className="h-5 w-5" />,
    color: 'accent'
  },
  {
    name: "Vivienda, Ciudad y Territorio",
    averageProgress: 45.2,
    totalIndicators: 5,
    completedIndicators: 2,
    icon: <Home className="h-5 w-5" />,
    color: 'primary'
  },
  {
    name: "Agricultura y Desarrollo Rural",
    averageProgress: 42.8,
    totalIndicators: 6,
    completedIndicators: 2,
    icon: <Leaf className="h-5 w-5" />,
    color: 'secondary'
  },
  {
    name: "Trabajo",
    averageProgress: 38.5,
    totalIndicators: 4,
    completedIndicators: 1,
    icon: <Building2 className="h-5 w-5" />,
    color: 'accent'
  },
  {
    name: "Transporte",
    averageProgress: 35.1,
    totalIndicators: 3,
    completedIndicators: 1,
    icon: <Wrench className="h-5 w-5" />,
    color: 'primary'
  },
  {
    name: "Gobierno Territorial",
    averageProgress: 32.7,
    totalIndicators: 8,
    completedIndicators: 2,
    icon: <Shield className="h-5 w-5" />,
    color: 'secondary'
  },
  {
    name: "Justicia y del Derecho",
    averageProgress: 28.9,
    totalIndicators: 3,
    completedIndicators: 1,
    icon: <Shield className="h-5 w-5" />,
    color: 'accent'
  },
  {
    name: "Minas y Energía",
    averageProgress: 25.4,
    totalIndicators: 3,
    completedIndicators: 1,
    icon: <Building2 className="h-5 w-5" />,
    color: 'primary'
  },
  {
    name: "Información y Estadísticas",
    averageProgress: 22.1,
    totalIndicators: 2,
    completedIndicators: 0,
    icon: <Building2 className="h-5 w-5" />,
    color: 'secondary'
  },
  {
    name: "Organismos de Control",
    averageProgress: 18.6,
    totalIndicators: 3,
    completedIndicators: 0,
    icon: <Building2 className="h-5 w-5" />,
    color: 'accent'
  }
];

const topDepartments = departmentData
  .sort((a, b) => b.averageProgress - a.averageProgress)
  .slice(0, 8);

const StatsSection: React.FC = () => {
  const [showAllDepartments, setShowAllDepartments] = useState(false);
  const displayData = showAllDepartments ? departmentData : topDepartments;
  const totalProgress = 52.8; // Promedio general de Cajicá

  return (
    <section className="w-full py-8">
      <div className="container mx-auto px-4">
        <div className="text-center mb-8">
          <h2 className="text-2xl md:text-3xl font-bold text-foreground font-institutional mb-4">
            Avances Plan de Desarrollo 2024-2027 - Promedio del 52.8% de Progreso General
          </h2>
          <p className="text-muted-foreground max-w-3xl mx-auto">
            Seguimiento transparente del progreso por sectores del Plan de Desarrollo Municipal &ldquo;Cajicá Ideal 2024-2027&rdquo;, 
            organizado en 5 dimensiones estratégicas y 18 sectores de inversión
          </p>
          <div className="mt-4 inline-flex items-center space-x-4 bg-primary/10 px-6 py-3 rounded-lg">
            <div className="text-center">
              <div className="text-2xl font-bold text-primary">{totalProgress.toFixed(1)}%</div>
              <div className="text-xs text-muted-foreground">Promedio General</div>
            </div>
            <div className="w-px h-8 bg-border"></div>
            <div className="text-center">
              <div className="text-2xl font-bold text-primary">{departmentData.length}</div>
              <div className="text-xs text-muted-foreground">Sectores</div>
            </div>
          </div>
        </div>
        
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
          {displayData.map((dept, index) => (
            <Card key={index} className="border-border hover:shadow-lg transition-shadow duration-300">
              <CardHeader className="pb-3">
                <div className="flex items-center justify-between">
                  <div className={`
                    p-2 rounded-lg 
                    ${dept.color === 'primary' ? 'bg-primary/10 text-primary' : ''}
                    ${dept.color === 'secondary' ? 'bg-secondary/10 text-secondary-foreground' : ''}
                    ${dept.color === 'accent' ? 'bg-accent text-accent-foreground' : ''}
                  `}>
                    {dept.icon}
                  </div>
                  <div className="text-right">
                    <span className="text-2xl font-bold text-foreground">
                      {dept.averageProgress.toFixed(1)}%
                    </span>
                    <div className="text-xs text-muted-foreground">promedio</div>
                  </div>
                </div>
                <CardTitle className="text-sm font-medium text-foreground leading-tight">
                  {dept.name}
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                <Progress 
                  value={dept.averageProgress} 
                  className="h-2"
                />
                <div className="space-y-1">
                  <div className="flex justify-between text-xs text-muted-foreground">
                    <span>Indicadores completados</span>
                    <span>{dept.completedIndicators}/{dept.totalIndicators}</span>
                  </div>
                  <div className="text-xs text-muted-foreground">
                    Eficiencia: {((dept.completedIndicators / dept.totalIndicators) * 100).toFixed(1)}%
                  </div>
                </div>
              </CardContent>
            </Card>
          ))}
        </div>

        {departmentData.length > 8 && (
          <div className="mt-8 text-center">
            <button
              onClick={() => setShowAllDepartments(!showAllDepartments)}
              className="inline-flex items-center space-x-2 px-6 py-3 bg-primary/10 hover:bg-primary/20 text-primary rounded-lg transition-colors duration-200 font-medium"
            >
              <span>{showAllDepartments ? 'Ver mejores 8 sectores' : `Ver todos los ${departmentData.length} sectores`}</span>
              {showAllDepartments ? <ChevronUp className="h-4 w-4" /> : <ChevronDown className="h-4 w-4" />}
            </button>
          </div>
        )}

        <div className="mt-8 text-center">
          <Card className="max-w-2xl mx-auto">
            <CardContent className="p-6">
              <div className="flex items-center justify-center space-x-2 text-muted-foreground">
                <Building2 className="h-5 w-5" />
                <span className="text-sm font-medium">
                  Datos actualizados - Plan de Desarrollo 2024-2027
                </span>
              </div>
              <div className="mt-2 text-xs text-muted-foreground">
                Basado en {departmentData.reduce((sum, dept) => sum + dept.totalIndicators, 0)} indicadores de gestión de {departmentData.length} sectores del Plan &ldquo;Cajicá Ideal 2024-2027&rdquo;
              </div>
              <div className="mt-1 text-xs text-muted-foreground">
                Promedio general de avance: {totalProgress.toFixed(1)}% • Indicadores completados: {departmentData.reduce((sum, dept) => sum + dept.completedIndicators, 0)} de {departmentData.reduce((sum, dept) => sum + dept.totalIndicators, 0)}
              </div>
              <div className="mt-1 text-xs text-muted-foreground font-medium">
                📊 Progreso por sectores municipales • 5 Dimensiones Estratégicas • Fuente: Alcaldía de Cajicá
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    </section>
  );
};

export default StatsSection;
