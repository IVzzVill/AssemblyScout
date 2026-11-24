import QtQuick 2.12

Rectangle {
  id: panel
  implicitWidth: 290
  implicitHeight: 405
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

  function labelForVariant(variant) {
    if (variant === "correct") return "Correcta"
    if (variant === "error_1") return "Error 1"
    return "Error 2"
  }



  Column {
    anchors.fill: parent
    anchors.margins: 12
    spacing: 8

    Text {
      text: "PROXIMIDAD"
      color: "#edf2f7"
      font.bold: true
      font.pixelSize: 15
    }

    Row {
      spacing: 8
      Rectangle { width: 15; height: 15; radius: 8; color: panel.colorFor(SafetyStatusPanel.frontState) }
      Text { text: "Frente · " + panel.labelFor(SafetyStatusPanel.frontState); color: "#edf2f7"; width: 159; font.pixelSize: 13 }
      Text { text: SafetyStatusPanel.frontDistance; color: "#b9c4d0"; font.pixelSize: 13 }
    }
    Row {
      spacing: 8
      Rectangle { width: 15; height: 15; radius: 8; color: panel.colorFor(SafetyStatusPanel.leftState) }
      Text { text: "Izquierda · " + panel.labelFor(SafetyStatusPanel.leftState); color: "#edf2f7"; width: 159; font.pixelSize: 13 }
      Text { text: SafetyStatusPanel.leftDistance; color: "#b9c4d0"; font.pixelSize: 13 }
    }
    Row {
      spacing: 8
      Rectangle { width: 15; height: 15; radius: 8; color: panel.colorFor(SafetyStatusPanel.rightState) }
      Text { text: "Derecha · " + panel.labelFor(SafetyStatusPanel.rightState); color: "#edf2f7"; width: 159; font.pixelSize: 13 }
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

    Rectangle { width: parent.width; height: 1; color: "#465464" }

    Text {
      text: "ESTADO DE ESTACIONES"
      color: "#edf2f7"
      font.bold: true
      font.pixelSize: 14
    }

    Text {
      text: "Estación 1 · " + panel.labelForVariant(SafetyStatusPanel.station1Variant)
      color: "#c9d5e0"
      font.pixelSize: 13
    }
    Row {
      spacing: 5
      Rectangle { width: 79; height: 27; radius: 4; color: SafetyStatusPanel.station1Variant === "correct" ? "#0c80bd" : "#344554"; border.width: 1; border.color: "#53697b"; Text { anchors.centerIn: parent; text: "Correcta"; color: "white"; font.pixelSize: 11 } MouseArea { anchors.fill: parent; onClicked: SafetyStatusPanel.SetStationVariant("station_1", "correct") } }
      Rectangle { width: 79; height: 27; radius: 4; color: SafetyStatusPanel.station1Variant === "error_1" ? "#0c80bd" : "#344554"; border.width: 1; border.color: "#53697b"; Text { anchors.centerIn: parent; text: "Error 1"; color: "white"; font.pixelSize: 11 } MouseArea { anchors.fill: parent; onClicked: SafetyStatusPanel.SetStationVariant("station_1", "error_1") } }
      Rectangle { width: 79; height: 27; radius: 4; color: SafetyStatusPanel.station1Variant === "error_2" ? "#0c80bd" : "#344554"; border.width: 1; border.color: "#53697b"; Text { anchors.centerIn: parent; text: "Error 2"; color: "white"; font.pixelSize: 11 } MouseArea { anchors.fill: parent; onClicked: SafetyStatusPanel.SetStationVariant("station_1", "error_2") } }
    }

    Text {
      text: "Estación 2 · " + panel.labelForVariant(SafetyStatusPanel.station2Variant)
      color: "#c9d5e0"
      font.pixelSize: 13
    }
    Row {
      spacing: 5
      Rectangle { width: 79; height: 27; radius: 4; color: SafetyStatusPanel.station2Variant === "correct" ? "#0c80bd" : "#344554"; border.width: 1; border.color: "#53697b"; Text { anchors.centerIn: parent; text: "Correcta"; color: "white"; font.pixelSize: 11 } MouseArea { anchors.fill: parent; onClicked: SafetyStatusPanel.SetStationVariant("station_2", "correct") } }
      Rectangle { width: 79; height: 27; radius: 4; color: SafetyStatusPanel.station2Variant === "error_1" ? "#0c80bd" : "#344554"; border.width: 1; border.color: "#53697b"; Text { anchors.centerIn: parent; text: "Error 1"; color: "white"; font.pixelSize: 11 } MouseArea { anchors.fill: parent; onClicked: SafetyStatusPanel.SetStationVariant("station_2", "error_1") } }
      Rectangle { width: 79; height: 27; radius: 4; color: SafetyStatusPanel.station2Variant === "error_2" ? "#0c80bd" : "#344554"; border.width: 1; border.color: "#53697b"; Text { anchors.centerIn: parent; text: "Error 2"; color: "white"; font.pixelSize: 11 } MouseArea { anchors.fill: parent; onClicked: SafetyStatusPanel.SetStationVariant("station_2", "error_2") } }
    }

    Text {
      width: parent.width
      text: "Cada selección sustituye la pieza centrada de su estación."
      wrapMode: Text.WordWrap
      color: "#8fa2b4"
      font.pixelSize: 11
    }


  }
}
