# AssemblyScout — Teleoperación con control PS4

Autor: Ivan Vazquez Villar

## Visión del proyecto

AssemblyScout busca desarrollar una plataforma móvil de inspección visual multivista de ensambles automotrices en laboratorio.

La teleoperación permite controlar manualmente la plataforma durante pruebas y preparación del sistema. La inspección visual, la navegación supervisada y el brazo posicionador de cámara pertenecen a etapas posteriores.

[Consultar la presentación general del proyecto](../../README.md)

## Alcance de la actividad 8

Esta actividad implementó un nodo que convierte las entradas del control PS4 en velocidades y un archivo launch que inicia el sistema completo con Turtlesim.

Posteriormente, el nodo se reutilizó para controlar el robot simulado en Gazebo mediante un tópico de velocidad configurable.

Estas pruebas no incluyen conducción del robot físico ni inspección visual implementada.

## Entorno y comunicación

Se utiliza ROS 2 Jazzy en Ubuntu.

El control fue detectado como Sony Interactive Entertainment Wireless Controller y conectado mediante USB.

El paquete joy proporciona el ejecutable game_controller_node, que publica las entradas en /joy mediante mensajes sensor_msgs/msg/Joy.

El campo axes contiene los valores analógicos y buttons contiene los estados digitales.

## Pruebas iniciales del control

Se inició el lector mediante:

    source /opt/ros/jazzy/setup.bash
    ros2 run joy game_controller_node --ros-args -p deadzone:=0.05 -p autorepeat_rate:=20.0

En otra terminal se observaron las entradas mediante:

    source /opt/ros/jazzy/setup.bash
    ros2 topic echo /joy --once --flow-style

Se movieron los sticks y se presionaron los controles individualmente.

| Entrada | Índice | Valor observado |
|---------|--------|-----------------|
| Stick izquierdo hacia adelante | axes[1] | Aproximadamente +0.96 |
| Stick derecho hacia la izquierda | axes[2] | +1.0 |
| R2 suelto | axes[5] | 0.0 |
| R2 completamente presionado | axes[5] | -1.0 |
| Botón X presionado | buttons[0] | 1 |
| Botón X suelto | buttons[0] | 0 |

## Decisiones de control

R2 controla el avance mediante axes[5] y L2 controla el retroceso mediante axes[4]. Sus valores negativos se convierten en presiones positivas.

La velocidad lineal se calcula restando la presión de L2 a la de R2 y multiplicando el resultado por la velocidad máxima. Si ambos gatillos tienen la misma presión, la velocidad lineal es cero.

El stick derecho horizontal, axes[2], controla el giro. Puede utilizarse al mismo tiempo que los gatillos o para girar en el lugar.

Al soltar todos los controles se envían velocidades cero. También se envía cero si dejan de recibirse mensajes válidos durante más de 0.5 segundos.

El botón X se identificó en buttons[0] y no tiene una acción asignada.

Los límites iniciales son 1.5 para velocidad lineal y 1.5 rad/s para velocidad angular. Los índices y límites son parámetros configurables.

## Estado actual

Se implementó el nodo ps4_teleop, que recibe sensor_msgs/msg/Joy en /joy y publica geometry_msgs/msg/Twist.

El parámetro cmd_vel_topic selecciona el destino: /turtle1/cmd_vel para Turtlesim y /cmd_vel para Gazebo.

### Ejecución con Turtlesim

    cd ~/assemblyscout_ws
    source /opt/ros/jazzy/setup.bash
    source install/setup.bash
    ros2 launch assemblyscout_teleop ps4_turtlesim.launch.py

### Integración con Gazebo

El launch de simulación configura la velocidad lineal máxima en 0.40 m/s y la angular en 2.00 rad/s.

[Consultar ejecución y documentación de Gazebo](../robot_description/README.md)


## Fuente consultada

[Documentación oficial del paquete joy](https://index.ros.org/p/joy/)


## Evidencia en video

Demostración de la teleoperación con el control PS4, la ejecución mediante launch y la comprobación del sistema en ROS 2.

[Ver video de AssemblyScout con control PS4](https://drive.google.com/file/d/1dwj4O0xD4h5nkd6FfjZFCcKPgAALWCe_/view?usp=sharing)
