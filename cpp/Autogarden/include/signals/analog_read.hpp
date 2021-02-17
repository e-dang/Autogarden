#pragma once

#include <Arduino.h>

#include <pins/interfaces/pin.hpp>
#include <signals/interfaces/signal.hpp>
#include <stdexcept>

class AnalogRead : public ISignal {
public:
    void execute(const ITerminalPin* pin) override {
        if (pin->getMode() != PinMode::AnalogInput)
            throw std::runtime_error("Pinmode must be AnalogInput to write to this pin");
        __mValue = analogRead(pin->getPinNum());
    }

    int getValue() const override {
        return __mValue;
    }

private:
    int __mValue;
};