#include <gz/gui/Plugin.hh>
#include <gz/gui/Application.hh>
#include <gz/gui/GuiEvents.hh>
#include <gz/gui/MainWindow.hh>
#include <gz/msgs/stringmsg.pb.h>
#include <gz/plugin/Register.hh>
#include <gz/transport/Node.hh>

#include <QJsonDocument>
#include <QJsonObject>
#include <QJsonValue>
#include <QMetaObject>
#include <QCoreApplication>
#include <QString>

namespace assemblyscout::gui
{
class SafetyStatusPanel : public gz::gui::Plugin
{
  Q_OBJECT
  Q_PROPERTY(QString frontState READ FrontState NOTIFY FrontStateChanged)
  Q_PROPERTY(QString leftState READ LeftState NOTIFY LeftStateChanged)
  Q_PROPERTY(QString rightState READ RightState NOTIFY RightStateChanged)
  Q_PROPERTY(QString frontDistance READ FrontDistance NOTIFY FrontDistanceChanged)
  Q_PROPERTY(QString leftDistance READ LeftDistance NOTIFY LeftDistanceChanged)
  Q_PROPERTY(QString rightDistance READ RightDistance NOTIFY RightDistanceChanged)

  public: QString FrontState() const { return this->frontState; }
  public: QString LeftState() const { return this->leftState; }
  public: QString RightState() const { return this->rightState; }
  public: QString FrontDistance() const { return this->frontDistance; }
  public: QString LeftDistance() const { return this->leftDistance; }
  public: QString RightDistance() const { return this->rightDistance; }

  public: Q_INVOKABLE void BeginBoxPlacement()
  {
    auto *app = gz::gui::App();
    if (!app)
      return;
    auto *window = app->findChild<gz::gui::MainWindow *>();
    if (!window)
      return;

    // Spawn recibe el evento y permite que la persona elija la posición con
    // un clic en el piso. La caja es estática para una prueba repetible.
    const std::string box = R"(
<sdf version="1.10">
  <model name="obstacle_box">
    <static>true</static>
    <link name="link">
      <collision name="collision"><geometry><box><size>0.18 0.18 0.18</size></box></geometry></collision>
      <visual name="visual"><geometry><box><size>0.18 0.18 0.18</size></box></geometry>
        <material><diffuse>0.95 0.35 0.10 1</diffuse><ambient>0.95 0.35 0.10 1</ambient></material>
      </visual>
    </link>
  </model>
</sdf>)";
    QCoreApplication::postEvent(
      window,
      new gz::gui::events::SpawnFromDescription(box));
  }

  signals: void FrontStateChanged();
  signals: void LeftStateChanged();
  signals: void RightStateChanged();
  signals: void FrontDistanceChanged();
  signals: void LeftDistanceChanged();
  signals: void RightDistanceChanged();

  protected: void LoadConfig(const tinyxml2::XMLElement *_pluginElem) override
  {
    this->Context()->setContextProperty("SafetyStatusPanel", this);

    std::string topic = "/assemblyscout/safety/status";
    if (_pluginElem)
    {
      if (const auto *topicElem = _pluginElem->FirstChildElement("topic"))
      {
        if (const auto *text = topicElem->GetText())
          topic = text;
      }
    }
    this->node.Subscribe(topic, &SafetyStatusPanel::OnMessage, this);
  }

  private: void OnMessage(const gz::msgs::StringMsg &_message)
  {
    const QString payload = QString::fromStdString(_message.data());
    QMetaObject::invokeMethod(this, [this, payload]()
    {
      const auto document = QJsonDocument::fromJson(payload.toUtf8());
      if (!document.isObject())
        return;
      const auto sensors = document.object().value("sensors").toObject();
      this->SetSensor("front", sensors.value("front").toObject());
      this->SetSensor("left", sensors.value("left").toObject());
      this->SetSensor("right", sensors.value("right").toObject());
    }, Qt::QueuedConnection);
  }

  private: void SetSensor(const QString &_name, const QJsonObject &_sensor)
  {
    const QString state = _sensor.value("state").toString("unknown");
    const auto distanceValue = _sensor.value("min_distance_m");
    const bool hasReading = _sensor.value("has_reading").toBool(false);
    const bool inRange = _sensor.value("in_range").toBool(false);
    const QString distance = !hasReading
      ? "sin lectura"
      : !inRange
        ? "> 4.00 m"
        : distanceValue.isDouble()
          ? QString::number(distanceValue.toDouble(), 'f', 2) + " m"
          : "sin lectura";

    if (_name == "front")
    {
      if (this->frontState != state) { this->frontState = state; emit FrontStateChanged(); }
      if (this->frontDistance != distance) { this->frontDistance = distance; emit FrontDistanceChanged(); }
    }
    else if (_name == "left")
    {
      if (this->leftState != state) { this->leftState = state; emit LeftStateChanged(); }
      if (this->leftDistance != distance) { this->leftDistance = distance; emit LeftDistanceChanged(); }
    }
    else
    {
      if (this->rightState != state) { this->rightState = state; emit RightStateChanged(); }
      if (this->rightDistance != distance) { this->rightDistance = distance; emit RightDistanceChanged(); }
    }
  }

  private: gz::transport::Node node;
  private: QString frontState{"unknown"};
  private: QString leftState{"unknown"};
  private: QString rightState{"unknown"};
  private: QString frontDistance{"sin lectura"};
  private: QString leftDistance{"sin lectura"};
  private: QString rightDistance{"sin lectura"};
};
}

GZ_ADD_PLUGIN(assemblyscout::gui::SafetyStatusPanel, gz::gui::Plugin)

#include "SafetyStatusPanel.moc"
