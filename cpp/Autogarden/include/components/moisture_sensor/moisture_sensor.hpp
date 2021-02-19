#pragma once

#include <components/moisture_sensor/interfaces/moisture_sensor.hpp>

class MoistureSensor : public IMoistureSensor {
public:
    MoistureSensor(const std::string& id, ILogicInputPin* inputPin, const float& scaler = 0.) :
        IMoistureSensor(id), __pPin(inputPin), __mScaler(scaler) {}

    ~MoistureSensor() = default;

    int readRaw() override {
        auto signal = std::make_shared<AnalogRead>();
        if (__pPin == nullptr || !__pPin->processSignal(signal) || !Component::_propagateSignal())
            return MoistureSensor::NULL_READ_VALUE;

        return signal->getValue();
    }

    float readScaled() override {
        return __mScaler * static_cast<float>(readRaw());
    }

protected:
    bool _setInputPins(Component* parent) override {
        auto parentOutputPins = _getComponentOutputPins(parent);
        if (parentOutputPins == nullptr)
            return false;

        return parentOutputPins->connect(__pPin.get());
    }

    IOutputPinSet* _getOutputPins() override {
        return nullptr;
    }

private:
    float __mScaler;
    std::unique_ptr<ILogicInputPin> __pPin;

    static const int NULL_READ_VALUE = INT32_MIN;
};