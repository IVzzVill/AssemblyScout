# LeakScout — Teleoperación con control PS4

Autor: Ivan Vazquez Villar

## Visión del proyecto

LeakScout busca desarrollar un sistema de inspección visual móvil basado en ROS 2 para observar puntos definidos alrededor de estaciones de mecanizado automotriz.

El alcance inicial propuesto es identificar cambios visuales compatibles con posibles acumulaciones de refrigerante o lubricante en un entorno de laboratorio y registrar ubicación, fecha y evidencia para revisión por mantenimiento.

No se plantea identificar químicamente el líquido ni diagnosticar la causa de una fuga.

## Alcance de la actividad 8

Esta actividad desarrolla la teleoperación con un control PS4 y la valida mediante Turtlesim.

Se construirá un nodo que convierta las entradas del control en velocidades y un archivo launch que inicie el sistema completo.

Esta entrega todavía no incluye conducción del robot físico ni detección visual de fugas.

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

Se implementó el nodo ps4_teleop, que recibe sensor_msgs/msg/Joy en /joy y publica geometry_msgs/msg/Twist en /turtle1/cmd_vel.

## Fuente consultada

[Documentación oficial del paquete joy](https://index.ros.org/p/joy/)


## Evidencia en video

Demostración de la teleoperación con el control PS4, la ejecución mediante launch y la comprobación del sistema en ROS 2.

[Ver video de LeakScout con control PS4](https://drive.google.com/file/d/1dwj4O0xD4h5nkd6FfjZFCcKPgAALWCe_/view?usp=sharing)
