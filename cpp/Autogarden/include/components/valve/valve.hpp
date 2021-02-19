#pragma once

#include <components/component.hpp>
#include <components/valve/interfaces/valve.hpp>
#include <signals/signals.hpp>

class Valve : public IValve {
public:
    Valve(const std::string& id, ILogicInputPin* inputPin, const int& onValue = HIGH, const int& offValue = LOW) :
        IValve(id), __pPin(inputPin), __mOnValue(onValue), __mOffValue(offValue) {}

    bool open() override {
        return _performAction(__mOnValue);
    }

    bool close() override {
        return _performAction(__mOffValue);
    }

protected:
    bool _setInputPins(Component* parent) override {
        auto parentOutputPins = _getComponentOutputPins(parent);
        if (parentOutputPins == nullptr)
            return false;

        parentOutputPins->connect(__pPin.get());
        return true;
    }

    IOutputPinSet* _getOutputPins() override {
        return nullptr;
    }

    bool _performAction(const int& value) {
        if (__pPin == nullptr || !__pPin->processSignal(std::make_shared<DigitalWrite>(value)))
            return false;

        return _propagateSignal();
    }

private:
    int __mOnValue;
    int __mOffValue;
    std::unique_ptr<ILogicInputPin> __pPin;
};