#pragma once

#include <components/component.hpp>
#include <components/valve/interfaces/valve.hpp>
#include <signals/signals.hpp>

class Valve : public Component, public IValve {
public:
    Valve(const std::string& id, const int& onValue = HIGH, const int& offValue = LOW,
          ILogicInputPin* inputPin = nullptr) :
        Component(id), __mOnValue(onValue), __mOffValue(offValue), __pPin(inputPin) {}

    bool open() override {
        return _performAction(__mOnValue);
    }

    bool close() override {
        return _performAction(__mOffValue);
    }

protected:
    bool _setInputPins(IOutputPinSet* parentOutputPins) override {
        if (parentOutputPins == nullptr)
            return false;

        parentOutputPins->connect(__pPin);
        return true;
    }

    IOutputPinSet* _getOutputPins() override {
        return nullptr;
    }

    bool _performAction(const int& value) {
        if (__pPin == nullptr)
            return false;

        DigitalWrite signal(value);
        __pPin->processSignal(&signal);
        return _propagateSignal();
    }

private:
    int __mOnValue;
    int __mOffValue;
    ILogicInputPin* __pPin;
};