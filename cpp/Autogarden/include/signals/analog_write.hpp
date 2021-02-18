#pragma once

#include <Arduino.h>

#include <pins/interfaces/pin.hpp>
#include <signals/interfaces/signal.hpp>
#include <stdexcept>

class AnalogWrite : public ISignal {
public:
    AnalogWrite(const int& value) : __mValue(value) {}

    ~AnalogWrite() = default;

    bool execute(const ITerminalPin* pin) override {
        if (pin->getMode() != PinMode::AnalogOutput)
            return false;
        analogWrite(pin->getPinNum(), __mValue);
        return true;
    }

    int getValue() const override {
        return __mValue;
    }

private:
    int __mValue;
};