# AssemblyScout

**Plataforma móvil para inspección visual multivista de arneses automotrices**

AssemblyScout es un proyecto en desarrollo para inspeccionar la presencia y
colocación exterior de componentes de un arnés automotriz mediante imágenes
obtenidas desde distintos puntos de vista.

La propuesta combina una base móvil, un brazo posicionador de cámara y una
aplicación local para conservar imágenes, resultados e historial. La evaluación
se realizará en un circuito predefinido de tres estaciones para el mismo tipo
de arnés.

## Objetivo del proyecto

El objetivo final es desplazar el robot entre estaciones de inspección, detener
la base, posicionar una cámara de detalle y capturar vistas previamente
definidas del arnés.

El sistema evaluará únicamente características exteriores visibles, como:

- Presencia de componentes
- Colocación exterior
- Orientación visible
- Posición aparente de clips, cable y conector

Los resultados utilizarán tres categorías:

- **Conforme en los puntos inspeccionados:** los criterios visuales definidos
  pudieron comprobarse
- **Anomalía detectada:** existe evidencia visual de una discrepancia
- **Inspección inconclusa:** la imagen, el enfoque o la visibilidad no permiten
  completar la evaluación

Una imagen deficiente o un punto oculto no demuestra ausencia ni conformidad.

El proyecto no comprobará continuidad eléctrica, crimpado interno, torque,
fuerza de retención ni características que no sean visibles.

## Arnés y estaciones

Se construirá un tramo representativo del arnés sobre un soporte sencillo,
priorizando facilidad de diseño CAD y fabricación física.

La configuración inicial contempla:

- Una placa rectangular con taladros y fijaciones
- Dos clips de guiado
- Un tramo de cable
- Un conector comercial

Las cantidades finales, dimensiones, materiales y componentes exactos se
definirán después de probar el enfoque de la cámara y el alcance del brazo.
Los componentes comerciales podrán representarse mediante envolventes
simplificadas en CAD.

No se fabricará una puerta ni se reproducirá el interior del conector.

El circuito tendrá tres estaciones para el mismo tipo de arnés. La distribución,
altura, orientación y número de ejemplares todavía están pendientes.

Las condiciones correctas y anómalas se rotarán entre ubicaciones para evitar
que una estación represente siempre el mismo defecto.

## Hardware seleccionado

| Elemento | Estado |
| --- | --- |
| Base móvil | Cuenta con modelo URDF, RViz, Gazebo y teleoperación PS4 |
| Logitech C920 | Cámara física montada en la base para observar el entorno |
| Brazo de Dipmecatrónica | Integrado dinámicamente en URDF, RViz y Gazebo con torreta, hombro y codo revolutos; faltan límites físicos y una interfaz de control propia |
| Cámara Yuju 14684 | Cámara física de detalle montada en el brazo; su representación visual en CAD y Gazebo conserva la geometría disponible de una Logitech C920 |

La lista compartida del brazo incluye cuatro servomotores MG995, estructura,
pinza, rodamientos y tornillería. Todavía deben confirmarse sus articulaciones
efectivas, límites, dimensiones y montaje. La pinza podrá sustituirse por un
soporte para cámara si las pruebas muestran que es viable.

El brazo posicionará la cámara con la base detenida. No manipulará ni reparará
el arnés.

La ficha compartida de la Yuju anuncia resolución 1080p, masa de 90 g y enfoque
desde aproximadamente 30 cm. Estos valores están pendientes de comprobación y
no representan resultados medidos por el proyecto.

## Funcionamiento previsto

1. Iniciar una misión y cargar la configuración del recorrido
2. Desplazar la base hasta una estación
3. Detener el robot
4. Posicionar la cámara mediante el brazo
5. Capturar las vistas definidas para el arnés
6. Evaluar los criterios exteriores visibles
7. Guardar imágenes, configuración y resultado
8. Permitir la consulta del historial y la evidencia

En una etapa posterior se desarrollarán evasión local y recuperación del
circuito dentro de condiciones validadas. Si no existe un paso viable, el robot
deberá detenerse y registrar el bloqueo.

## Estado actual

### Implementado

| Componente | Avance |
| --- | --- |
| Teleoperación con PS4 | Control de avance, retroceso y giro, probado en Turtlesim y Gazebo |
| Nodo de teleoperación | Conversión de mensajes `/joy` en comandos `/assemblyscout/cmd_vel` |
| Modelo URDF | Representación del chasis y las dos ruedas |
| Brazo y cámara de detalle | Torreta, brazo y antebrazo con cámara integrados dinámicamente y sostenidos en la postura CAD inicial |
| Visualización en RViz | Modelo articulado y ejes de referencia |
| Simulación en Gazebo | Propiedades físicas, colisiones simplificadas y movimiento |
| Control diferencial | Conversión de velocidad lineal y angular en movimiento de ruedas |
| Comunicación ROS 2–Gazebo | Intercambio de velocidad, odometría, estados articulares, transformaciones y reloj |
| Archivos launch | Inicio de los componentes de cada demostración |
| Evidencias | Videos de teleoperación, RViz y Gazebo, además del grafo de comunicación |

La simulación y la teleoperación corresponden a antecedentes técnicos del
proyecto. La conducción y validación sobre el robot físico siguen pendientes.

### Seleccionado o definido

- Arnés automotriz como objeto de inspección
- Circuito predefinido de tres estaciones
- Brazo de Dipmecatrónica
- Cámara Yuju 14684
- Conservación de la Logitech C920 en la base
- Configuración inicial del soporte representativo
- Categorías de resultados
- Estructura prevista para el registro de evidencia

El brazo y la cámara de detalle ya están representados en los archivos URDF,
RViz y Gazebo. La Yuju física, su soporte definitivo, el soporte del arnés y
las estaciones permanecen pendientes de validación e integración física.

## Arquitectura implementada

```text
Control PS4
    |
    v
game_controller_node
    |  /joy
    v
ps4_teleop
    |  /assemblyscout/cmd_vel
    v
ros_gz_bridge
    |
    v
Control diferencial de Gazebo
    |
    +-- /odom
    +-- /joint_states
    +-- /tf
          |
          v
         RViz
```

Los controles actuales son:

- **R2:** avanzar
- **L2:** retroceder
- **Stick derecho horizontal:** girar
- **Controles sueltos:** velocidad cero

## Aplicación y registro

Se plantea una aplicación local sencilla para consultar historial,
imágenes/resultados y un asistente. No incluirá editor de circuitos, mapas ni
control directo de actuadores.

El registro previsto utilizará:

- Un archivo JSON por inspección
- Imágenes organizadas en carpetas
- Un manifiesto por recorrido
- Exportación CSV derivada

Los registros conservarán identificadores de misión, estación, arnés o sesión,
punto, vista, fecha, configuración y resultado.

Se preverá un único proceso escritor, uso de archivos temporales y recuperación
de registros incompletos. No se utilizarán SQL ni SQLite.

## Asistente

El asistente podrá consultar y resumir evidencia recuperada mediante código.

Deberá:

- Utilizar conteos deterministas
- Referenciar registros e imágenes
- Reconocer cuando faltan datos

No podrá:

- Enviar comandos de movimiento
- Modificar evidencia
- Declarar conformidad

El modelo, proveedor y ejecución local o mediante API siguen pendientes. La
inspección, el registro y la consulta convencional deberán funcionar sin el
asistente.

## Trabajo pendiente

- Definir dimensiones y materiales finales del soporte del arnés
- Fabricar la placa, fijaciones, clips y montaje del conector
- Confirmar los ejes, límites físicos y dimensiones finales del brazo
- Diseñar y validar el soporte físico para la Yuju
- Verificar las características reales de la cámara
- Calibrar la cámara y las transformaciones del sistema
- Definir puntos y vistas de inspección
- Construir y distribuir físicamente las tres estaciones
- Transferir y validar el control en el robot físico
- Implementar captura e inspección visual
- Desarrollar evasión local y recuperación del circuito
- Implementar el registro de evidencia
- Desarrollar la aplicación local
- Incorporar posteriormente el asistente
- Comparar una vista y múltiples vistas mediante pruebas documentadas

## Organización del repositorio

```text
AssemblyScout/
├── README.md
└── src/
    ├── assemblyscout_teleop/
    │   └── README.md
    └── robot_description/
        └── README.md
```

- [Teleoperación con PS4](src/assemblyscout_teleop/README.md): entradas del
  control, nodo de velocidad, ejecución y video
- [Modelo del robot, RViz y Gazebo](src/robot_description/README.md): mallas,
  URDF, propiedades físicas, comandos, problemas, soluciones y evidencias

Los README internos documentan las entregas técnicas anteriores y se conservan
sin modificaciones.

## Documentación técnica

| Contenido | Documento |
| --- | --- |
| Herramientas y dependencias | [Modelo, RViz y Gazebo](src/robot_description/README.md#herramientas-utilizadas) |
| Modificaciones del modelo | [Modelo, RViz y Gazebo](src/robot_description/README.md#modificaciones-realizadas-al-modelo) |
| Arquitectura de comunicación | [Modelo, RViz y Gazebo](src/robot_description/README.md#arquitectura-de-comunicación) |
| Compilación y ejecución | [Modelo, RViz y Gazebo](src/robot_description/README.md#compilación) |
| Problemas y soluciones | [Modelo, RViz y Gazebo](src/robot_description/README.md#problemas-encontrados-y-soluciones) |
| Configuración del PS4 | [Teleoperación con PS4](src/assemblyscout_teleop/README.md) |

Los comandos, videos y evidencias permanecen en los documentos técnicos
correspondientes.

## Tecnologías actuales

- Ubuntu 24.04
- ROS 2 Jazzy
- Python
- URDF
- RViz
- Gazebo Harmonic
- `ros_gz`
- SolidWorks
- Control PS4

## Autor

Ivan Vazquez Villar
