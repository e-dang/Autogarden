#pragma once

#include <components/liquid_level_sensor/interfaces/liquid_level_sensor.hpp>

class LiquidLevelSensor : public ILiquidLevelSensor {
public:
    ~LiquidLevelSensor() = default;

    LiquidLevelSensor(const String& id, ILogicInputPin* inputPin, const int& okValue = HIGH) :
        ILiquidLevelSensor(id), __pPin(inputPin), __mOkValue(okValue) {}

    const char* read() override {
        auto signal = std::make_shared<DigitalRead>();
        if (__pPin == nullptr || !__pPin->processSignal(signal) || !_propagateSignal())
            return nullptr;

        return signal->getValue() == __mOkValue ? OK_VALUE : LOW_VALUE;
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
    int __mOkValue;
    std::unique_ptr<ILogicInputPin> __pPin;
};
