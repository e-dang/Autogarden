#pragma once

#include <Arduino.h>

#include <pins/interfaces/pin.hpp>
#include <signals/interfaces/signal.hpp>
#include <stdexcept>

class DigitalWrite : public ISignal {
public:
    DigitalWrite(const int& value) : __mValue(value) {}

    ~DigitalWrite() = default;

    bool execute(const ITerminalPin* pin) override {
        if (pin->getMode() != PinMode::DigitalOutput)
            return false;
        digitalWrite(pin->getPinNum(), __mValue);
        return true;
    }

    int getValue() const override {
        return __mValue;
    }

private:
    int __mValue;
};