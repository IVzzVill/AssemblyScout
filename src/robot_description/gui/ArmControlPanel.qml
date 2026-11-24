import QtQuick 2.12
import QtQuick.Controls 2.12

Rectangle {
  implicitWidth: 290
  implicitHeight: 460
  color: "#1b222b"
  radius: 8
  border.width: 1
  border.color: "#465464"

  Column {
    anchors.fill: parent
    anchors.margins: 12
    spacing: 8

    Text { text: "BRAZO Y CÁMARA"; color: "#edf2f7"; font.bold: true; font.pixelSize: 15 }
    Text {
      width: parent.width
      text: "Ajuste manual con la base detenida. La postura de reposo es la inicial del CAD."
      wrapMode: Text.WordWrap; color: "#a8b7c6"; font.pixelSize: 12
    }

    Rectangle {
      width: parent.width; height: 30; radius: 4
      color: restMouse.pressed ? "#0c80bd" : "#12a7e0"
      Text { anchors.centerIn: parent; text: "Volver a reposo"; color: "white"; font.bold: true; font.pixelSize: 13 }
      MouseArea { id: restMouse; anchors.fill: parent; onClicked: ArmControlPanel.SendArmToRest() }
    }

    Text { text: "POSTURAS DE INSPECCIÓN"; color: "#d7e1ea"; font.bold: true; font.pixelSize: 12 }
    Row {
      spacing: 8
      Rectangle {
        width: 129; height: 29; radius: 4; color: station1Mouse.pressed ? "#0c80bd" : "#34546a"
        Text { anchors.centerIn: parent; text: "Estación 1"; color: "white"; font.pixelSize: 12 }
        MouseArea { id: station1Mouse; anchors.fill: parent; onClicked: ArmControlPanel.SendArmToStation1() }
      }
      Rectangle {
        width: 129; height: 29; radius: 4; color: station2Mouse.pressed ? "#0c80bd" : "#34546a"
        Text { anchors.centerIn: parent; text: "Estación 2"; color: "white"; font.pixelSize: 12 }
        MouseArea { id: station2Mouse; anchors.fill: parent; onClicked: ArmControlPanel.SendArmToStation2() }
      }
    }

    Text { text: "Torreta · " + ArmControlPanel.turretReference.toFixed(2) + " rad"; color: "#d7e1ea"; font.pixelSize: 12 }
    Slider {
      width: parent.width; from: -3.14; to: 3.14; value: ArmControlPanel.turretReference
      onMoved: ArmControlPanel.SetArmReference("turret", value)
    }

    Text { text: "Hombro · " + ArmControlPanel.shoulderReference.toFixed(2) + " rad"; color: "#d7e1ea"; font.pixelSize: 12 }
    Slider {
      width: parent.width; from: -3.14; to: 3.14; value: ArmControlPanel.shoulderReference
      onMoved: ArmControlPanel.SetArmReference("shoulder", value)
    }

    Text { text: "Codo · " + ArmControlPanel.elbowReference.toFixed(2) + " rad"; color: "#d7e1ea"; font.pixelSize: 12 }
    Slider {
      // El extremo +/-pi deja al antebrazo cerca de una configuración
      // singular del CAD. Se reserva para calibración, no para operación.
      width: parent.width; from: -1.75; to: 1.75; value: ArmControlPanel.elbowReference
      onMoved: ArmControlPanel.SetArmReference("elbow", value)
    }

    Text {
      width: parent.width
      text: "El codo usa un rango operativo seguro. Ajusta una vista, anota sus tres valores y después la guardaremos como vista de estación."
      wrapMode: Text.WordWrap; color: "#8fa2b4"; font.pixelSize: 11
    }
  }
}
