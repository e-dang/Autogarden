#pragma once

#include <Arduino.h>

#include <pins/interfaces/pin.hpp>
#include <signals/interfaces/signal.hpp>
#include <stdexcept>

class DigitalRead : public ISignal {
public:
    DigitalRead() : __mValue(-1) {}

    ~DigitalRead() = default;

    void execute(const ITerminalPin* pin) override {
        if (pin->getMode() != PinMode::DigitalInput)
            throw std::runtime_error("Pinmode must be DigitalInput to write to this pin");
        __mValue = digitalRead(pin->getPinNum());
    }

    int getValue() const {
        return __mValue;
    }

private:
    int __mValue;
};