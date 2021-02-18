#pragma once

#include <components/component.hpp>
#include <components/valve/interfaces/valve.hpp>
#include <signals/signals.hpp>

class Valve : public IValve {
public:
    Valve(const std::string& id, ILogicInputPin* inputPin, const int& onValue = HIGH, const int& offValue = LOW) :
        Component(id), __pPin(inputPin), __mOnValue(onValue), __mOffValue(offValue) {}

    bool open() override {
        return _performAction(__mOnValue);
    }

    bool close() override {
        return _performAction(__mOffValue);
    }

    IOutputPinSet* getOutputPins() override {
        return nullptr;
    }

protected:
    bool _setInputPins(Component* parent) override {
        auto parentOutputPins = parent->getOutputPins();
        if (parentOutputPins == nullptr)
            return false;

        parentOutputPins->connect(__pPin.get());
        return true;
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
    std::unique_ptr<ILogicInputPin> __pPin;
};