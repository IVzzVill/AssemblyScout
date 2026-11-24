#include <gz/gui/Plugin.hh>
#include <gz/msgs/double.pb.h>
#include <gz/plugin/Register.hh>
#include <gz/transport/Node.hh>

#include <QMetaObject>
#include <QString>
#include <QTimer>

#include <algorithm>

namespace assemblyscout::gui
{
class ArmControlPanel : public gz::gui::Plugin
{
  Q_OBJECT
  Q_PROPERTY(double turretReference READ TurretReference NOTIFY TurretReferenceChanged)
  Q_PROPERTY(double shoulderReference READ ShoulderReference NOTIFY ShoulderReferenceChanged)
  Q_PROPERTY(double elbowReference READ ElbowReference NOTIFY ElbowReferenceChanged)

  public: double TurretReference() const { return this->turretReference; }
  public: double ShoulderReference() const { return this->shoulderReference; }
  public: double ElbowReference() const { return this->elbowReference; }

  public: Q_INVOKABLE void SetArmReference(
      const QString &_joint, const double _radians)
  {
    double target = std::clamp(_radians, -3.14159265359, 3.14159265359);
    gz::transport::Node::Publisher *publisher = nullptr;

    if (_joint == "turret")
    {
      this->turretReference = target;
      emit TurretReferenceChanged();
      publisher = &this->turretPublisher;
    }
    else if (_joint == "shoulder")
    {
      this->shoulderReference = target;
      emit ShoulderReferenceChanged();
      publisher = &this->shoulderPublisher;
    }
    else if (_joint == "elbow")
    {
      // Evita pedir la postura extrema +/-pi desde la interfaz. En esa zona
      // el brazo CAD pierde ventaja mecánica y parece no responder.
      target = std::clamp(target, -1.75, 1.75);
      this->elbowReference = target;
      emit ElbowReferenceChanged();
      publisher = &this->elbowPublisher;
    }
    else
    {
      return;
    }

    if (!*publisher)
      return;

    gz::msgs::Double command;
    command.set_data(target);
    publisher->Publish(command);
  }

  public: Q_INVOKABLE void SendArmToRest()
  {
    this->SendArmToPose(0.0, 0.0, 0.0);
  }

  public: Q_INVOKABLE void SendArmToStation1()
  {
    // Referencia tomada de la primera prueba visual frente a estación 1.
    this->SendArmToPose(-0.13, -1.30, 0.58);
  }

  public: Q_INVOKABLE void SendArmToStation2()
  {
    // Referencia tomada de la primera prueba visual frente a estación 2.
    this->SendArmToPose(0.0, -1.25, 0.76);
  }

  private: void SendArmToPose(const double _turret, const double _shoulder,
      const double _elbow)
  {
    this->SetArmReference("turret", _turret);
    this->SetArmReference("shoulder", _shoulder);
    this->SetArmReference("elbow", _elbow);

    // Repite la referencia breve y explícitamente: el brazo es dinámico y los
    // controladores reciben así una orden fiable al soltar una vista.
    QTimer::singleShot(100, this, [this, _turret, _shoulder, _elbow]() {
      this->PublishPose(_turret, _shoulder, _elbow);
    });
    QTimer::singleShot(250, this, [this, _turret, _shoulder, _elbow]() {
      this->PublishPose(_turret, _shoulder, _elbow);
    });
  }

  signals: void TurretReferenceChanged();
  signals: void ShoulderReferenceChanged();
  signals: void ElbowReferenceChanged();

  protected: void LoadConfig(const tinyxml2::XMLElement *) override
  {
    this->Context()->setContextProperty("ArmControlPanel", this);
    this->turretPublisher = this->node.Advertise<gz::msgs::Double>(
      "/assemblyscout/arm/turret_position");
    this->shoulderPublisher = this->node.Advertise<gz::msgs::Double>(
      "/assemblyscout/arm/shoulder_position");
    this->elbowPublisher = this->node.Advertise<gz::msgs::Double>(
      "/assemblyscout/arm/elbow_position");
  }

  private: void PublishPose(const double _turret, const double _shoulder,
      const double _elbow)
  {
    this->SetArmReference("turret", _turret);
    this->SetArmReference("shoulder", _shoulder);
    this->SetArmReference("elbow", _elbow);
  }

  private: gz::transport::Node node;
  private: gz::transport::Node::Publisher turretPublisher;
  private: gz::transport::Node::Publisher shoulderPublisher;
  private: gz::transport::Node::Publisher elbowPublisher;
  private: double turretReference{0.0};
  private: double shoulderReference{0.0};
  private: double elbowReference{0.0};
};
}

GZ_ADD_PLUGIN(assemblyscout::gui::ArmControlPanel, gz::gui::Plugin)

#include "ArmControlPanel.moc"
