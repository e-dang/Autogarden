#pragma once

#include <components/moisture_sensor/interfaces/factory.hpp>
#include <components/moisture_sensor/moisture_sensor.hpp>

class MoistureSensorFactory : public IMoistureSensorFactory {
public:
    std::unique_ptr<IMoistureSensor> create(const std::string& id, const float& scaler) override {
        auto inputPin = __mInputPinFactory.createPin(0, PinMode::AnalogInput);
        return std::make_unique<MoistureSensor>(id, inputPin.release(), scaler);
    }

private:
    PinFactory<LogicInputPinSet, LogicInputPin> __mInputPinFactory;
};