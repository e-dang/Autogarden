#pragma once

#include <Arduino.h>

#include <pins/interfaces/pin.hpp>
#include <signals/interfaces/signal.hpp>
#include <stdexcept>

class DigitalWrite : public ISignal {
public:
    DigitalWrite(const int& value) : __mValue(value) {}

    ~DigitalWrite() = default;

    void execute(const ITerminalPin* pin) override {
        if (pin->getMode() != PinMode::DigitalOutput)
            throw std::runtime_error("Pinmode must be DigitalOutput to write to this pin");
        digitalWrite(pin->getPinNum(), __mValue);
    }

private:
    int __mValue;
};