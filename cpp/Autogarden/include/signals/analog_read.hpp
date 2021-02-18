#pragma once

#include <Arduino.h>

#include <pins/interfaces/pin.hpp>
#include <signals/interfaces/signal.hpp>
#include <stdexcept>

class AnalogRead : public ISignal {
public:
    bool execute(const ITerminalPin* pin) override {
        if (pin->getMode() != PinMode::AnalogInput)
            return false;

        __mValue = analogRead(pin->getPinNum());
        return true;
    }

    int getValue() const override {
        return __mValue;
    }

private:
    int __mValue;
};