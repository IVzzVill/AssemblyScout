cmake_minimum_required(VERSION 3.8)
project(robot_description)

find_package(ament_cmake REQUIRED)
find_package(gz-gui8 REQUIRED)
find_package(gz-transport13 REQUIRED)
find_package(gz-plugin2 REQUIRED COMPONENTS register)
find_package(gz-msgs10 REQUIRED)
find_package(Qt5 REQUIRED COMPONENTS Core)

set(CMAKE_AUTOMOC ON)
set(CMAKE_AUTORCC ON)

add_library(SafetyStatusPanel SHARED
  gui/SafetyStatusPanel.cc
  gui/SafetyStatusPanel.qrc
)

add_library(ArmControlPanel SHARED
  gui/ArmControlPanel.cc
  gui/ArmControlPanel.qrc
)

target_link_libraries(SafetyStatusPanel
  gz-gui8::core
  gz-transport13::core
  gz-plugin2::register
  gz-msgs10::core
  Qt5::Core
)

target_link_libraries(ArmControlPanel
  gz-gui8::core
  gz-transport13::core
  gz-plugin2::register
  gz-msgs10::core
  Qt5::Core
)

install(TARGETS SafetyStatusPanel ArmControlPanel
  LIBRARY DESTINATION lib
)

# Instala las mallas y los archivos de configuración del robot
install(
  DIRECTORY meshes urdf launch rviz scripts worlds
  DESTINATION share/${PROJECT_NAME}
)

ament_package()
