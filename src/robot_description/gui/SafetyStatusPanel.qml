import QtQuick 2.12

Rectangle {
  id: panel
  implicitWidth: 260
  implicitHeight: 180
  color: "#1b222b"
  radius: 8
  border.width: 1
  border.color: "#465464"

  function colorFor(state) {
    if (state === "free") return "#35bd69"
    if (state === "caution") return "#f4be3e"
    if (state === "blocked") return "#df4b4b"
    return "#88929e"
  }

  function labelFor(state) {
    if (state === "free") return "LIBRE"
    if (state === "caution") return "CERCA"
    if (state === "blocked") return "OBSTÁCULO"
    return "SIN LECTURA"
  }

  Column {
    anchors.fill: parent
    anchors.margins: 12
    spacing: 9

    Text {
      text: "PROXIMIDAD"
      color: "#edf2f7"
      font.bold: true
      font.pixelSize: 15
    }

    Row {
      spacing: 9
      Rectangle { width: 16; height: 16; radius: 8; color: panel.colorFor(SafetyStatusPanel.frontState) }
      Text { text: "Frente  ·  " + panel.labelFor(SafetyStatusPanel.frontState); color: "#edf2f7"; width: 142; font.pixelSize: 13 }
      Text { text: SafetyStatusPanel.frontDistance; color: "#b9c4d0"; font.pixelSize: 13 }
    }
    Row {
      spacing: 9
      Rectangle { width: 16; height: 16; radius: 8; color: panel.colorFor(SafetyStatusPanel.leftState) }
      Text { text: "Izquierda  ·  " + panel.labelFor(SafetyStatusPanel.leftState); color: "#edf2f7"; width: 142; font.pixelSize: 13 }
      Text { text: SafetyStatusPanel.leftDistance; color: "#b9c4d0"; font.pixelSize: 13 }
    }
    Row {
      spacing: 9
      Rectangle { width: 16; height: 16; radius: 8; color: panel.colorFor(SafetyStatusPanel.rightState) }
      Text { text: "Derecha  ·  " + panel.labelFor(SafetyStatusPanel.rightState); color: "#edf2f7"; width: 142; font.pixelSize: 13 }
      Text { text: SafetyStatusPanel.rightDistance; color: "#b9c4d0"; font.pixelSize: 13 }
    }

    Rectangle {
      width: parent.width
      height: 29
      radius: 4
      color: boxMouse.pressed ? "#0c80bd" : "#12a7e0"
      Text {
        anchors.centerIn: parent
        text: "Añadir caja"
        color: "white"
        font.bold: true
        font.pixelSize: 13
      }
      MouseArea {
        id: boxMouse
        anchors.fill: parent
        onClicked: SafetyStatusPanel.BeginBoxPlacement()
      }
    }
  }
}
