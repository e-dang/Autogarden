#pragma once

#include <Arduino.h>

#include <pins/interfaces/pin.hpp>
#include <signals/interfaces/signal.hpp>
#include <stdexcept>

class AnalogWrite : public ISignal {
public:
    AnalogWrite(const int& value) : __mValue(value) {}

    ~AnalogWrite() = default;

    void execute(const ITerminalPin* pin) override {
        if (pin->getMode() != PinMode::AnalogOutput)
            throw std::runtime_error("Pinmode must be AnalogOutput to write to this pin");
        analogWrite(pin->getPinNum(), __mValue);
    }

private:
    int __mValue;
};