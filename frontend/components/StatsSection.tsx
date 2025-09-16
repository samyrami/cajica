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
    name: "Secretaría de TIC",
    averageProgress: 48.8,
    totalIndicators: 10,
    completedIndicators: 3,
    icon: <Building2 className="h-5 w-5" />,
    color: 'primary'
  },
  {
    name: "Indersantander",
    averageProgress: 43.65,
    totalIndicators: 14,
    completedIndicators: 4,
    icon: <Users className="h-5 w-5" />,
    color: 'secondary'
  },
  {
    name: "Secretaría de Planeación",
    averageProgress: 43.02,
    totalIndicators: 19,
    completedIndicators: 8,
    icon: <Building2 className="h-5 w-5" />,
    color: 'accent'
  },
  {
    name: "Secretaría de Educación",
    averageProgress: 41.2,
    totalIndicators: 21,
    completedIndicators: 8,
    icon: <GraduationCap className="h-5 w-5" />,
    color: 'primary'
  },
  {
    name: "Secretaría Administrativa",
    averageProgress: 36.11,
    totalIndicators: 13,
    completedIndicators: 4,
    icon: <Building2 className="h-5 w-5" />,
    color: 'secondary'
  },
  {
    name: "Secretaría de Desarrollo Social",
    averageProgress: 32.44,
    totalIndicators: 16,
    completedIndicators: 4,
    icon: <Users className="h-5 w-5" />,
    color: 'accent'
  },
  {
    name: "Secretaría del Interior",
    averageProgress: 28.15,
    totalIndicators: 52,
    completedIndicators: 18,
    icon: <Shield className="h-5 w-5" />,
    color: 'primary'
  },
  {
    name: "Oficina para la Gestión del Riesgo de Desastres",
    averageProgress: 27.60,
    totalIndicators: 10,
    completedIndicators: 3,
    icon: <Shield className="h-5 w-5" />,
    color: 'secondary'
  },
  {
    name: "Secretaría de Salud",
    averageProgress: 26.89,
    totalIndicators: 54,
    completedIndicators: 12,
    icon: <Heart className="h-5 w-5" />,
    color: 'accent'
  },
  {
    name: "Secretaría Ambiental",
    averageProgress: 24.97,
    totalIndicators: 28,
    completedIndicators: 3,
    icon: <Leaf className="h-5 w-5" />,
    color: 'primary'
  },
  {
    name: "Secretaría de la Mujer y Equidad de Género",
    averageProgress: 24.46,
    totalIndicators: 15,
    completedIndicators: 2,
    icon: <Users className="h-5 w-5" />,
    color: 'secondary'
  },
  {
    name: "Secretaría de Infraestructura",
    averageProgress: 22.8,
    totalIndicators: 53,
    completedIndicators: 15,
    icon: <Wrench className="h-5 w-5" />,
    color: 'accent'
  },
  {
    name: "Secretaría de Cultura y Turismo",
    averageProgress: 18.74,
    totalIndicators: 21,
    completedIndicators: 2,
    icon: <Building2 className="h-5 w-5" />,
    color: 'primary'
  },
  {
    name: "Secretaría de Competitividad y Productividad",
    averageProgress: 15.11,
    totalIndicators: 11,
    completedIndicators: 1,
    icon: <Building2 className="h-5 w-5" />,
    color: 'secondary'
  },
  {
    name: "Secretaría de Hacienda",
    averageProgress: 14.90,
    totalIndicators: 2,
    completedIndicators: 0,
    icon: <Building2 className="h-5 w-5" />,
    color: 'accent'
  },
  {
    name: "Secretaría de Vivienda",
    averageProgress: 9.42,
    totalIndicators: 6,
    completedIndicators: 0,
    icon: <Home className="h-5 w-5" />,
    color: 'primary'
  },
  {
    name: "Secretaría de Agricultura y Desarrollo Rural",
    averageProgress: 0.89,
    totalIndicators: 28,
    completedIndicators: 1,
    icon: <Leaf className="h-5 w-5" />,
    color: 'secondary'
  }
];

const topDepartments = departmentData
  .sort((a, b) => b.averageProgress - a.averageProgress)
  .slice(0, 8);

const StatsSection: React.FC = () => {
  const [showAllDepartments, setShowAllDepartments] = useState(false);
  const displayData = showAllDepartments ? departmentData : topDepartments;
  const totalProgress = 25.0; // Promedio general real del 25%

  return (
    <section className="w-full py-8">
      <div className="container mx-auto px-4">
        <div className="text-center mb-8">
          <h2 className="text-2xl md:text-3xl font-bold text-foreground font-institutional mb-4">
            Avances en Objetivos Estratégicos 2025 - Promedio del 25% de Progreso General
          </h2>
          <p className="text-muted-foreground max-w-3xl mx-auto">
            Seguimiento transparente del progreso promedio de indicadores por dependencias de la Gobernación de Santander, 
            basado en el Plan de Desarrollo Departamental "Es Tiempo de Santander 2024-2027"
          </p>
          <div className="mt-4 inline-flex items-center space-x-4 bg-primary/10 px-6 py-3 rounded-lg">
            <div className="text-center">
              <div className="text-2xl font-bold text-primary">{totalProgress.toFixed(1)}%</div>
              <div className="text-xs text-muted-foreground">Promedio General</div>
            </div>
            <div className="w-px h-8 bg-border"></div>
            <div className="text-center">
              <div className="text-2xl font-bold text-primary">{departmentData.length}</div>
              <div className="text-xs text-muted-foreground">Dependencias</div>
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
              <span>{showAllDepartments ? 'Ver mejores 8 dependencias' : `Ver todas las ${departmentData.length} dependencias`}</span>
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
                  Datos actualizados al 10 de septiembre de 2025
                </span>
              </div>
              <div className="mt-2 text-xs text-muted-foreground">
                Basado en {departmentData.reduce((sum, dept) => sum + dept.totalIndicators, 0)} indicadores de gestión de {departmentData.length} dependencias del PDD "Es Tiempo de Santander"
              </div>
              <div className="mt-1 text-xs text-muted-foreground">
                Promedio general de avance de todos los indicadores: {totalProgress.toFixed(1)}% • Indicadores completados: {departmentData.reduce((sum, dept) => sum + dept.completedIndicators, 0)}
              </div>
              <div className="mt-1 text-xs text-muted-foreground font-medium">
                📊 Los porcentajes mostrados representan el promedio de avance por dependencia • Fuente: Informes oficiales de gestión
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    </section>
  );
};

export default StatsSection;
