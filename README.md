# AssemblyScout

**Plataforma móvil para inspección visual multivista de ensambles automotrices**

AssemblyScout es un proyecto en desarrollo que busca verificar la presencia y colocación visible de componentes de un ensamble automotriz mediante imágenes tomadas desde distintas posiciones.

La propuesta combina una base móvil, un brazo posicionador de cámara y una aplicación para organizar rutas, consultar evidencia y dar seguimiento a las inspecciones. Su evaluación se realizará en un entorno de laboratorio con tres estaciones del mismo tipo de ensamble.

Actualmente se cuenta con teleoperación mediante PS4, un modelo articulado del robot y simulación en Gazebo. La inspección visual, el brazo, la navegación supervisada y la aplicación corresponden a las siguientes etapas.

## Problema que busca resolver

Una sola imagen puede dejar puntos ocultos o ambiguos debido a la geometría del ensamble, reflejos o posición de la cámara. También es necesario conservar la relación entre una observación, la pieza inspeccionada y sus revisiones posteriores.

AssemblyScout propone obtener varias vistas de puntos definidos y registrar la evidencia de cada inspección. Se evaluará si las vistas adicionales permiten verificar más componentes y qué costo implican en tiempo, complejidad y recursos.

## Funcionamiento previsto

1. Configurar las estaciones, la ruta y los puntos de inspección
2. Desplazar el robot de forma supervisada hasta cada estación
3. Detener la base y posicionar la cámara en vistas previamente validadas
4. Capturar imágenes y evaluar los criterios visuales definidos
5. Guardar resultados y evidencia vinculados con la pieza
6. Permitir al operador revisar hallazgos, registrar intervenciones y solicitar una reinspección

Los resultados distinguirán entre:

- **Conforme en los puntos inspeccionados:** se verificaron los criterios visuales definidos
- **Anomalía detectada:** existe evidencia de una discrepancia
- **Inspección inconclusa:** la evidencia disponible no permite completar la evaluación

No observar un componente no demuestra que esté ausente ni permite aprobarlo.

## Avances actuales

| Componente | Avance |
| --- | --- |
| Teleoperación con PS4 | Control de avance, retroceso y giro, probado en Turtlesim y Gazebo |
| Modelo URDF | Representación del chasis y dos ruedas con articulaciones continuas |
| Visualización en RViz | Modelo articulado y comprobación de sus ejes de referencia |
| Simulación en Gazebo Harmonic | Incorporación de masas, centros de masa, inercias y colisiones simplificadas |
| Control diferencial | Conversión de comandos de velocidad en movimiento de las ruedas |
| Comunicación ROS 2–Gazebo | Intercambio de velocidades, odometría, estados articulares, transformaciones y reloj |
| Parada por pérdida del mando | Comprobada en simulación |
| Archivos launch | Arranque de los componentes necesarios para cada demostración |

La base de simulación permite probar el movimiento y la comunicación entre componentes. La integración y validación sobre el robot físico siguen pendientes.

## Arquitectura actual

    Control PS4
        |
        v
    Lectura del mando -> /joy
        |
        v
    Nodo de teleoperación -> /cmd_vel
        |
        v
    Puente ROS 2–Gazebo
        |
        v
    Control diferencial -> Movimiento del robot simulado
        |
        +-- Odometría
        +-- Estados articulares -> Transformaciones del robot

Los controles actuales son:

- **R2:** avanzar
- **L2:** retroceder
- **Stick derecho horizontal:** girar
- **Controles sueltos:** enviar velocidad cero

## Próximas etapas

- Definir el ensamble de prueba, sus puntos y anomalías observables
- Implementar una primera inspección desde una posición fija
- Seleccionar el brazo, la cámara de detalle, los soportes y la alimentación
- Evaluar la repetibilidad de las vistas y la calidad de las imágenes
- Integrar navegación supervisada entre tres estaciones y respuesta ante obstáculos
- Desarrollar la aplicación para rutas, misiones, evidencia e historial
- Incorporar consultas del historial mediante un asistente con referencias verificables
- Comparar una vista y múltiples vistas mediante pruebas documentadas

El registro de imágenes, configuraciones y resultados acompañará las primeras pruebas de inspección.

## Alcance

El proyecto se enfocará en características visibles, como presencia, variante y orientación de componentes. La selección definitiva del ensamble dependerá de la disponibilidad y de la posibilidad de observar sus puntos de interés.

La cámara integrada Logitech C920 se conservará para observar el entorno y apoyar la navegación. Se plantea incorporar una cámara ligera de detalle, posicionada por un brazo con la base detenida. El brazo, la cámara adicional y su montaje todavía están por seleccionar.

El brazo tendrá una función de observación, sin manipulación ni reparación de piezas. La evaluación se realizará en laboratorio y documentará los límites de lo que pueda comprobarse.

## Organización del repositorio

    AssemblyScout/
    ├── README.md
    └── src/
        ├── assemblyscout_teleop/
        │   └── README.md
        └── robot_description/
            └── README.md

- [Teleoperación con PS4](src/assemblyscout_teleop/README.md): lectura de las entradas del mando y conversión en comandos de velocidad
- [Modelo del robot, RViz y Gazebo](src/robot_description/README.md): mallas, modelo URDF, propiedades físicas y ejecución del sistema

Cada paquete incluye su documentación con dependencias, comandos de ejecución, comprobaciones y evidencias. El workspace local se denomina `assemblyscout_ws`.

## Documentación de entrega

La documentación técnica solicitada se encuentra en los README de cada
paquete y se conserva junto con el código correspondiente:

| Contenido | Documento |
| --- | --- |
| Herramientas y dependencias utilizadas | [Modelo del robot, RViz y Gazebo](src/robot_description/README.md#herramientas-utilizadas) |
| Modificaciones realizadas al modelo | [Modelo del robot, RViz y Gazebo](src/robot_description/README.md#modificaciones-realizadas-al-modelo) |
| Arquitectura de comunicación | [Modelo del robot, RViz y Gazebo](src/robot_description/README.md#arquitectura-de-comunicación) |
| Compilación y comandos de ejecución | [Modelo del robot, RViz y Gazebo](src/robot_description/README.md#compilación) |
| Problemas encontrados y soluciones | [Modelo del robot, RViz y Gazebo](src/robot_description/README.md#problemas-encontrados-y-soluciones) |
| Configuración y pruebas del control PS4 | [Teleoperación con PS4](src/assemblyscout_teleop/README.md) |

Los videos de las actividades, el grafo de comunicación y las comprobaciones
con comandos de ROS 2 se encuentran en esos documentos técnicos.

## Tecnologías utilizadas

- Ubuntu 24.04 y ROS 2 Jazzy
- Python y URDF
- RViz y Gazebo Harmonic
- `ros_gz` para comunicación entre ROS 2 y Gazebo
- SolidWorks para geometría y propiedades físicas
- Control PS4 para teleoperación

## Autor

Ivan Vazquez Villar
