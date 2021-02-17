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

    void initialize() override {
        auto mode = getMode();
        if (mode == PinMode::DigitalOutput || mode == PinMode::AnalogOutput) {
            pinMode(getPinNum(), mode);
            return;
        } else if (mode == PinMode::DigitalInput || mode == PinMode::AnalogInput) {
            pinMode(getPinNum(), mode);
            return;
        }

        throw std::runtime_error("Pin mode not recongized - " + std::to_string(mode));
    }

    bool processSignal(ISignal* signal) override {
        signal->execute(this);
        return true;
    }
};