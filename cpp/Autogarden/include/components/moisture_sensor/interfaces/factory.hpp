#pragma once

#include <components/moisture_sensor/interfaces/moisture_sensor.hpp>

class IMoistureSensorFactory {
public:
    virtual ~IMoistureSensorFactory() = default;

    virtual std::unique_ptr<IMoistureSensor> create(const std::string& id, const float& scaler) = 0;
};