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

El stick izquierdo vertical controlará el avance y retroceso.

El stick derecho horizontal controlará el giro.

R2 habilitará el movimiento cuando axes[5] sea menor que -0.5. Al soltar R2, se enviarán velocidades cero.

El botón X se identificó como entrada digital y no tiene una acción asignada por ahora.

Los índices, las velocidades máximas y el umbral de R2 serán configurables para facilitar cambios durante las pruebas y la demostración en clase.

## Estado actual

Se comprobó la lectura del control y se creó la estructura inicial del paquete. El nodo de teleoperación y el launch se desarrollarán en las siguientes etapas.

## Fuente consultada

[Documentación oficial del paquete joy](https://index.ros.org/p/joy/)
