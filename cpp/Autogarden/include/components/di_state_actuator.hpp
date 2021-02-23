#pragma once

#include <components/component.hpp>

class DiStateActuator : public Component {
public:
    DiStateActuator() = default;

    DiStateActuator(const String& id, ILogicInputPin* inputPin, const int& onValue, const int& offValue) :
        Component(id), __pPin(inputPin), _mOnValue(onValue), _mOffValue(offValue) {}

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

    bool _performAction(const int& value) {
        if (__pPin == nullptr || !__pPin->processSignal(std::make_shared<DigitalWrite>(value)))
            return false;

        return _propagateSignal();
    }

protected:
    int _mOnValue;
    int _mOffValue;

private:
    std::unique_ptr<ILogicInputPin> __pPin;
};
