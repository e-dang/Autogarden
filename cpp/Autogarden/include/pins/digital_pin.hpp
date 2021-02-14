#pragma once

#include <Arduino.h>

#include <pins/terminal_pin.hpp>

class DigitalPin : public TerminalPin {
public:
    DigitalPin(const uint8_t& pin, const int& value = LOW) : TerminalPin(pin, value) {}

    ~DigitalPin() = default;

    PinMode getMode() const override {
        return Digital;
    }

    void setValue(const int& value) override {
        Pin::setValue(value);
        _mIsStale = true;
    }

    void refresh() override {
        digitalWrite(getPin(), getValue());
        _mIsStale = false;
    }

protected:
    int _scaleValue(const int& value) override {
        return value > LOW ? HIGH : LOW;
    }
};