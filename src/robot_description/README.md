# LeakScout — Modelo del robot en RViz

## Descripción

Esta actividad integra el modelo de COLMIBOT al workspace LeakScout
mediante el paquete robot_description de ROS 2 Jazzy. El modelo permite
visualizar el chasis y controlar los ángulos de las dos ruedas motrices
en RViz mediante Joint State Publisher GUI.

## Preparación del modelo

Se utilizaron archivos STL exportados desde SolidWorks. Se revisaron
las mallas en MeshLab para comprobar que el chasis no incluyera las
dos ruedas motrices.

Las mallas originales utilizan milímetros. En el URDF se aplica una
escala de 0.001 en los tres ejes para representarlas en metros.

Las ruedas exportadas tienen coordenadas locales. Su colocación se
obtuvo revisando la geometría del STL del ensamble completo y se
comprobó visualmente en RViz.

## Estructura del paquete

- meshes/: mallas del chasis y las dos ruedas
- urdf/robot.urdf: enlaces, geometría y articulaciones
- launch/display.launch.py: inicio del sistema
- rviz/display.rviz: configuración de visualización
- CMakeLists.txt: instalación de los archivos del paquete
- package.xml: dependencias del paquete

## Decisiones y simplificaciones

El chasis agrupa la estructura, los motores, la electrónica, la cámara
y los apoyos esféricos. Estos elementos se representan como un conjunto
fijo para esta actividad.

Las ruedas se representan mediante dos articulaciones de tipo continuous:
wheel_left_joint y wheel_right_joint. Esto permite girarlas sin límites
angulares mecánicos definidos en el URDF.

Se utiliza base_link como referencia del robot, con X hacia el frente,
Y hacia la izquierda y Z hacia arriba. El enlace cad_link conserva
el montaje de las mallas y se conecta a base_link mediante una
articulación fija que ajusta la orientación del ensamble.

Los colores se asignan mediante materiales del URDF.

Esta versión está destinada a visualización y comprobación cinemática.
No incluye geometría de colisión, propiedades inerciales, simulación
física ni desplazamiento del robot.

## Dependencias

Se utiliza Ubuntu 24.04 con ROS 2 Jazzy, colcon y los paquetes de
visualización y publicación de estados.

Instalación de las herramientas necesarias, partiendo de ROS 2 Jazzy:

    sudo apt install python3-colcon-common-extensions ros-jazzy-ament-cmake ros-jazzy-launch-ros ros-jazzy-ament-index-python ros-jazzy-robot-state-publisher ros-jazzy-joint-state-publisher-gui ros-jazzy-rviz2

MeshLab se utilizó para inspeccionar las mallas; no es necesario para
ejecutar el launch.

## Compilación y ejecución

Desde una terminal:

    cd ~/leakscout_ws
    source /opt/ros/jazzy/setup.bash
    colcon build --packages-select robot_description
    source install/setup.bash
    QT_QPA_PLATFORM=xcb ros2 launch robot_description display.launch.py

El launch inicia:

- robot_state_publisher: publica la descripción y las transformaciones
- joint_state_publisher_gui: permite modificar los ángulos de las ruedas
- rviz2: muestra el modelo con la configuración guardada

La variable QT_QPA_PLATFORM=xcb selecciona el backend X11 de Qt.
Se utilizó en este equipo para evitar problemas de inicialización gráfica.

Se debe mantener una sola ejecución del launch. Para detenerla,
se presiona Ctrl+C en la terminal correspondiente.

## Comprobación

En otra terminal:

    source /opt/ros/jazzy/setup.bash
    ros2 node list
    ros2 topic info /joint_states
    ros2 topic info /tf
    ros2 topic echo /joint_states --once

Se verificó que /joint_states y /tf tuvieran un publicador cada uno,
y que los mensajes incluyeran wheel_left_joint y wheel_right_joint.

Al mover cada deslizador, la rueda correspondiente gira sobre su centro
sin separarse del chasis. RViz muestra Global Status: Ok.

Durante las pruebas se detectó parpadeo al mantener varias ejecuciones
simultáneas. Se resolvió deteniendo los launches anteriores e iniciando
una sola instancia.

## Evidencia en video

[Ver video del modelo y las articulaciones en RViz](https://drive.google.com/file/d/18gwdypMfG76y5TjWGCVo_H3EmoUbDE0k/view?usp=drive_link)

## Autor

Ivan Vazquez Villar
