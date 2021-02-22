#pragma once

#include <components/moisture_sensor/interfaces/moisture_sensor.hpp>

class MoistureSensor : public IMoistureSensor {
public:
    MoistureSensor(const String& id, ILogicInputPin* inputPin, const float& scaler = 0.) :
        IMoistureSensor(id), __pPin(inputPin), __mScaler(scaler) {}

    ~MoistureSensor() = default;

    int readRaw() override {
        auto signal = std::make_shared<AnalogRead>();
        if (__pPin == nullptr || !__pPin->processSignal(signal) || !_propagateSignal())
            return MoistureSensor::NULL_READ_VALUE;

        return signal->getValue();
    }

    float readScaled() override {
        auto rawVal = readRaw();
        if (rawVal == MoistureSensor::NULL_READ_VALUE)
            return static_cast<float>(rawVal);

        return __mScaler * static_cast<float>(rawVal);
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

public:
    static const int NULL_READ_VALUE = INT32_MIN;

private:
    float __mScaler;
    std::unique_ptr<ILogicInputPin> __pPin;
};