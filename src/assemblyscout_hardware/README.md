# Base física y brazo

Este paquete prepara la conexión entre ROS 2 y el ESP32. El puente de prueba
acepta el mismo tópico `/assemblyscout/cmd_vel` que usa Gazebo; todavía no
activa motores físicos ni genera odometría hasta medir encoder, ruedas y sentido
de cada motor.

## Brazo con tres MG995

La propuesta de señales del ESP32 reserva pines actualmente libres en el mapa
del equipo. Debe verificarse en la shield antes de conectar los servos:

| Articulación | GPIO propuesto | Función |
|---|---:|---|
| Torreta | GPIO 16 | PWM de posición |
| Hombro | GPIO 17 | PWM de posición |
| Codo | GPIO 5 | PWM de posición |

Los tres cables de señal de los MG995 van a esos GPIO. El cable rojo de cada
servo va a una fuente exclusiva de 5 a 6 V y el cable negro o café va al GND de
esa fuente. El GND de esa fuente debe unirse una sola vez al GND del ESP32 para
compartir referencia de señal.

No alimentar los MG995 desde el pin 5 V de la Raspberry Pi, el ESP32 ni el
convertidor de 5 A actualmente destinado a la electrónica de la base. Para tres
servos se requiere una fuente o BEC independiente de 5 a 6 V, con margen real
para picos de corriente; como punto de partida, 10 A. Conviene colocar fusible,
interruptor de corte y un capacitor de al menos 1000 uF cerca de la distribución
del brazo.

Antes de montar el brazo completo:

1. Probar un solo servo sin carga, con una posición central segura.
2. Confirmar sentido y rango mecánico de cada articulación.
3. Medir los pulsos PWM que corresponden a reposo y a cada vista de inspección.
4. Conectar los tres servos y validar que la caída de tensión no reinicie ESP32
   ni Raspberry Pi.

Las posiciones del brazo en Gazebo se expresan en radianes. La relación entre
esos ángulos y los pulsos PWM físicos se calibrará por articulación; no se debe
suponer que es idéntica para los tres MG995.
