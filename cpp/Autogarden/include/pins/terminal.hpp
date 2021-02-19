#pragma once

#include <Arduino.h>

#include <pins/interfaces/terminal.hpp>
#include <pins/output.hpp>
#include <signals/signals.hpp>
#include <string>

class TerminalPin : public OutputPin, public ITerminalPin {
public:
    TerminalPin(const int& pinNum, const PinMode& pinMode) : OutputPin(pinNum, pinMode) {}

    ~TerminalPin() = default;

    bool initialize() override {
        auto mode = getMode();
        if (mode == PinMode::DigitalOutput || mode == PinMode::AnalogOutput) {
            pinMode(getPinNum(), OUTPUT);
            return true;
        } else if (mode == PinMode::DigitalInput || mode == PinMode::AnalogInput) {
            pinMode(getPinNum(), INPUT);
            return true;
        }

        return false;
    }

    bool processSignal(std::shared_ptr<ISignal> signal) override {
        return signal->execute(this);
    }
};