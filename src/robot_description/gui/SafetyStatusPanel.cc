#include <gz/gui/Plugin.hh>
#include <gz/gui/Application.hh>
#include <gz/gui/GuiEvents.hh>
#include <gz/gui/MainWindow.hh>
#include <gz/msgs/boolean.pb.h>
#include <gz/msgs/entity.pb.h>
#include <gz/msgs/entity_factory.pb.h>
#include <gz/msgs/stringmsg.pb.h>
#include <gz/plugin/Register.hh>
#include <gz/transport/Node.hh>

#include <QCoreApplication>
#include <QJsonDocument>
#include <QJsonObject>
#include <QMetaObject>
#include <QString>

#include <string>

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
  Q_PROPERTY(QString station1Variant READ Station1Variant NOTIFY Station1VariantChanged)
  Q_PROPERTY(QString station2Variant READ Station2Variant NOTIFY Station2VariantChanged)

  public: QString FrontState() const { return this->frontState; }
  public: QString LeftState() const { return this->leftState; }
  public: QString RightState() const { return this->rightState; }
  public: QString FrontDistance() const { return this->frontDistance; }
  public: QString LeftDistance() const { return this->leftDistance; }
  public: QString RightDistance() const { return this->rightDistance; }
  public: QString Station1Variant() const { return this->station1Variant; }
  public: QString Station2Variant() const { return this->station2Variant; }

  public: Q_INVOKABLE void BeginBoxPlacement()
  {
    auto *app = gz::gui::App();
    if (!app)
      return;
    auto *window = app->findChild<gz::gui::MainWindow *>();
    if (!window)
      return;

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

  public: Q_INVOKABLE void SetStationVariant(
      const QString &_station, const QString &_variant)
  {
    if ((_station != "station_1" && _station != "station_2") ||
        (_variant != "correct" && _variant != "error_1" && _variant != "error_2"))
      return;

    const std::string station = _station.toStdString();
    const std::string variant = _variant.toStdString();
    const std::string modelName = "inspection_" + station + "_piece";

    gz::msgs::Entity request;
    request.set_name(modelName);
    request.set_type(gz::msgs::Entity::MODEL);

    auto callback = std::function<void(const gz::msgs::Boolean &, const bool)>(
      [this, station, variant](const gz::msgs::Boolean &_reply, const bool _result)
      {
        if (!_result || !_reply.data())
          return;
        this->CreateStationPiece(station, variant);
      });
    this->node.Request(
      "/world/assemblyscout_inspection_cell/remove", request, callback);
  }


  signals: void FrontStateChanged();
  signals: void LeftStateChanged();
  signals: void RightStateChanged();
  signals: void FrontDistanceChanged();
  signals: void LeftDistanceChanged();
  signals: void RightDistanceChanged();
  signals: void Station1VariantChanged();
  signals: void Station2VariantChanged();

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

  private: std::string PieceSdf(
      const std::string &_station, const std::string &_variant) const
  {
    std::string mesh;
    double centerX = 0.0;
    double visualZ = 0.0;
    double collisionZ = 0.0;
    double sizeX = 0.0;
    double sizeY = 0.0;
    double sizeZ = 0.0;
    double stationX = 0.0;
    double stationY = 0.0;

    if (_station == "station_1")
    {
      stationX = 1.20;
      stationY = 0.55;
      centerX = 0.007586;
      visualZ = 0.0075;
      sizeX = 0.115172;
      sizeY = 0.099872;
      if (_variant == "correct")
      {
        mesh = "DiscoCorrectoC1.STL";
        sizeZ = 0.017000;
        collisionZ = 0.008500;
      }
      else if (_variant == "error_1")
      {
        mesh = "DiscoErrorC1_1.STL";
        centerX = 0.0075765;
        sizeX = 0.115153;
        sizeZ = 0.013500;
        collisionZ = 0.006750;
      }
      else
      {
        mesh = "DiscoErrorC1_2.STL";
        sizeZ = 0.016508;
        collisionZ = 0.008254;
      }
    }
    else
    {
      stationX = 2.20;
      stationY = -0.55;
      centerX = 0.0173715;
      visualZ = 0.0125;
      sizeX = 0.134743;
      sizeY = 0.099872;
      if (_variant == "correct" || _variant == "error_1")
      {
        mesh = _variant == "correct" ? "DiscoCorrectoC2.STL" : "DiscoErrorC2_1.STL";
        sizeZ = 0.027000;
        collisionZ = 0.013500;
      }
      else
      {
        mesh = "DiscoErrorC2_2.STL";
        sizeZ = 0.022000;
        collisionZ = 0.011000;
      }
    }

    const std::string modelName = "inspection_" + _station + "_piece";
    return "<sdf version='1.10'><model name='" + modelName + "'>"
      "<static>true</static><pose>" + std::to_string(stationX) + " " +
      std::to_string(stationY) + " 0.240 0 0 0</pose><link name='link'>"
      "<collision name='inspection_collision'><pose>0 0 " +
      std::to_string(collisionZ) + " 0 0 0</pose><geometry><box><size>" +
      std::to_string(sizeX) + " " + std::to_string(sizeY) + " " +
      std::to_string(sizeZ) + "</size></box></geometry></collision>"
      "<visual name='inspection_visual'><pose>" + std::to_string(centerX) +
      " 0 " + std::to_string(visualZ) + " 0 0 0</pose><geometry><mesh><uri>"
      "model://robot_description/meshes/inspection/versions/" + mesh +
      "</uri><scale>0.001 0.001 0.001</scale></mesh></geometry>"
      "<material><ambient>0.52 0.56 0.60 1</ambient><diffuse>0.52 0.56 0.60 1</diffuse></material>"
      "</visual></link></model></sdf>";
  }

  private: void CreateStationPiece(
      const std::string &_station, const std::string &_variant)
  {
    gz::msgs::EntityFactory request;
    request.set_sdf(this->PieceSdf(_station, _variant));
    auto callback = std::function<void(const gz::msgs::Boolean &, const bool)>(
      [this, station = _station, variant = _variant](
        const gz::msgs::Boolean &_reply, const bool _result)
      {
        if (!_result || !_reply.data())
          return;
        QMetaObject::invokeMethod(this, [this, station, variant]()
        {
          if (station == "station_1")
          {
            this->station1Variant = QString::fromStdString(variant);
            emit Station1VariantChanged();
          }
          else
          {
            this->station2Variant = QString::fromStdString(variant);
            emit Station2VariantChanged();
          }
        }, Qt::QueuedConnection);
      });
    this->node.Request(
      "/world/assemblyscout_inspection_cell/create", request, callback);
  }

  private: gz::transport::Node node;
  private: QString frontState{"unknown"};
  private: QString leftState{"unknown"};
  private: QString rightState{"unknown"};
  private: QString frontDistance{"sin lectura"};
  private: QString leftDistance{"sin lectura"};
  private: QString rightDistance{"sin lectura"};
  private: QString station1Variant{"correct"};
  private: QString station2Variant{"correct"};
};
}

GZ_ADD_PLUGIN(assemblyscout::gui::SafetyStatusPanel, gz::gui::Plugin)

#include "SafetyStatusPanel.moc"
