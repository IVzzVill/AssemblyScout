# AssemblyScout

**Plataforma móvil para inspección visual multivista en una celda de ensamble.**

AssemblyScout desarrolla una base móvil con brazo posicionador para acercar una
cámara a puntos de inspección. La simulación actual representa una celda de
prueba con dos estaciones, una banda estática que las conecta y sensores de
proximidad para validar la circulación antes de llevar el diseño al robot
físico.

## Objetivo del proyecto

El objetivo es que el robot se desplace entre estaciones, se detenga de forma
segura, coloque la cámara de detalle en vistas definidas y conserve la
evidencia de la inspección. La primera pieza de trabajo es un conjunto de freno
impreso en 3D; sus modelos CAD definitivos sustituirán los elementos temporales
actuales de la simulación.

La inspección evaluará solamente aspectos exteriores visibles: presencia,
posición y orientación aparente de los componentes. Los resultados previstos
son:

- **Conforme en los puntos inspeccionados**
- **Anomalía detectada**
- **Inspección inconclusa**

Una zona oculta o una imagen insuficiente no prueba ni ausencia ni
conformidad. El proyecto no pretende verificar propiedades internas, fuerza,
torque o continuidad eléctrica.

## Estado actual

### Implementado y probado en simulación

- Base móvil diferencial con dos ruedas, URDF, RViz y Gazebo Harmonic.
- Teleoperación PS4 para avance, retroceso y giro.
- Brazo dinámico con torreta, hombro y codo, conservando su postura inicial y
  respuesta física al movimiento de la base.
- Dos cámaras contempladas en el modelo: Logitech C920 para observar el entorno
  desde la base y Yuju 14684 como cámara de detalle en el brazo.
- Celda de inspección con dos estaciones elevadas, marcas de ruta y una banda
  estática en forma de Z que conecta las estaciones sin cubrir las superficies
  de inspección.
- Tres sensores láser simulados: frontal, izquierdo y derecho.
- Panel de proximidad en Gazebo que muestra por sensor una distancia real,
  estado libre/cerca/obstáculo y permite insertar cajas de prueba.
- Filtro de seguridad: las lecturas frontales reducen o detienen únicamente el
  avance; las laterales informan proximidad sin bloquear el giro para permitir
  maniobrar y evitar un obstáculo.
- Comunicación entre ROS 2, Gazebo, el control y RViz.

Las estaciones usan por ahora mallas temporales de componentes de freno. No se
consideran el ensamble final ni resultados de inspección hasta recibir e
integrar el CAD definitivo.

### Pendiente

- Recibir e integrar las piezas CAD finales en STL, con sus dimensiones y
  posiciones de montaje reales.
- Definir las configuraciones correcta y anómala de cada estación, y una
  interfaz para alternarlas durante las pruebas.
- Calibrar los puntos de inspección y las vistas de ambas cámaras.
- Validar dimensiones, límites y soporte físico definitivo del brazo y la
  cámara Yuju.
- Crear navegación autónoma, evasión local y recuperación del recorrido.
- Capturar imágenes, evaluar visualmente las piezas y registrar evidencia.
- Implementar el historial local, exportación y asistente de consulta.
- Transferir y validar el sistema en el robot físico.

## Arquitectura de comunicación

```text
Control PS4
   │  /joy
   ▼
ps4_teleop
   │  /assemblyscout/cmd_vel_raw
   ▼
safety_gate ◄── sensores láser frontal, izquierdo y derecho
   │  /assemblyscout/cmd_vel
   ▼
ros_gz_bridge
   ▼
Gazebo: control diferencial, odometría y estados articulares
   │
   ├── /odom, /joint_states, /tf ──► RViz
   └── /assemblyscout/safety/status ──► Panel Proximidad de Gazebo
```

El nodo `safety_gate` es el único que entrega velocidad al control diferencial.
Así se evita que una orden anterior continúe moviendo la base y se mantiene una
ruta clara entre el control y la simulación.

## Ejecución

Desde la raíz del workspace:

```bash
cd ~/assemblyscout_ws
source /opt/ros/jazzy/setup.bash
source install/setup.bash
ros2 launch robot_description gazebo.launch.py
```

El lanzamiento abre Gazebo, RViz y la teleoperación con PS4. Para iniciar sin
RViz o sin acomodar las ventanas:

```bash
ros2 launch robot_description gazebo.launch.py use_rviz:=false arrange_windows:=false
```

Los controles actuales son:

- **R2:** avanzar
- **L2:** retroceder
- **Stick derecho horizontal:** girar
- **Controles sueltos:** velocidad cero

Para probar detección sin modificar el mundo, usa el botón **Añadir caja** del
panel **Proximidad** de Gazebo. La caja es un obstáculo físico: la distancia que
muestra cada sensor procede de su lectura láser, no de una distancia fijada en
la interfaz.

## Organización del repositorio

```text
AssemblyScout/
├── README.md
└── src/
    ├── assemblyscout_teleop/   # Control PS4 y filtro de seguridad
    └── robot_description/     # URDF, mallas, mundos, launch, RViz y Gazebo
```

Los README internos conservan la documentación técnica y las evidencias de las
entregas anteriores:

- [Teleoperación con PS4](src/assemblyscout_teleop/README.md)
- [Modelo del robot, RViz y Gazebo](src/robot_description/README.md)

## Tecnologías actuales

- Ubuntu 24.04
- ROS 2 Jazzy
- Python
- URDF y SDF
- Gazebo Harmonic y `ros_gz`
- RViz
- SolidWorks
- Control PS4

## Autor

Ivan Vazquez Villar
