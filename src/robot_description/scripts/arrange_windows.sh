#!/usr/bin/env bash

# Coloca Gazebo y RViz en mitades opuestas del escritorio disponible
if ! command -v wmctrl >/dev/null 2>&1; then
  echo '[arrange_windows] wmctrl no está instalado; se conserva la posición actual'
  exit 0
fi

for _ in $(seq 1 15); do
  windows=$(wmctrl -lx 2>/dev/null)
  gazebo_id=$(printf '%s\n' "$windows" | awk '/gz-sim-gui\.Gazebo GUI/ {print $1; exit}')
  rviz_id=$(printf '%s\n' "$windows" | awk '/rviz2\.rviz2/ {print $1; exit}')

  work_area=$(wmctrl -d 2>/dev/null | awk '
    $2 == "*" {
      for (i = 1; i <= NF; i++) {
        if ($i == "WA:") {
          print $(i + 1), $(i + 2)
          exit
        }
      }
    }
  ')

  # Wayland puede ocultar las propiedades del escritorio a wmctrl
  if [ -z "$work_area" ]; then
    screen_size=$(xdpyinfo 2>/dev/null | awk '/dimensions:/ {print $2; exit}')
    if [ -z "$screen_size" ]; then
      screen_size=$(xrandr --current 2>/dev/null | awk '/\*/ {print $1; exit}')
    fi
    if [[ "$screen_size" =~ ^[0-9]+x[0-9]+$ ]]; then
      work_area="0,0 $screen_size"
    fi
  fi

  if [ -n "$gazebo_id" ] && [ -n "$rviz_id" ] && [ -n "$work_area" ]; then
    read -r origin size <<< "$work_area"
    origin_x=${origin%,*}
    origin_y=${origin#*,}
    width=${size%x*}
    height=${size#*x}
    left_width=$((width / 2))
    right_width=$((width - left_width))
    right_x=$((origin_x + left_width))

    wmctrl -ir "$gazebo_id" -b remove,maximized_vert,maximized_horz,fullscreen
    wmctrl -ir "$rviz_id" -b remove,maximized_vert,maximized_horz,fullscreen
    sleep 0.2
    wmctrl -ir "$gazebo_id" -e "0,$origin_x,$origin_y,$left_width,$height"
    wmctrl -ir "$rviz_id" -e "0,$right_x,$origin_y,$right_width,$height"
    echo '[arrange_windows] Gazebo y RViz acomodados'
    exit 0
  fi

  sleep 1
done

echo '[arrange_windows] No se encontraron ambas ventanas; se conserva su posición actual'
exit 0
