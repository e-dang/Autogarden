#pragma once

#include <Arduino.h>

#include <pins/interfaces/pin.hpp>
#include <signals/interfaces/signal.hpp>
#include <stdexcept>

class DigitalRead : public ISignal {
public:
    DigitalRead() : __mValue(-1) {}

    ~DigitalRead() = default;

    bool execute(const ITerminalPin* pin) override {
        if (pin->getMode() != PinMode::DigitalInput)
            return false;
        __mValue = digitalRead(pin->getPinNum());
        return true;
    }

    int getValue() const override {
        return __mValue;
    }

private:
    int __mValue;
};