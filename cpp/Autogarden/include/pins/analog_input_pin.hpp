#pragma once

#include <Arduino.h>

#include <pins/terminal_pin.hpp>

class AnalogInputPin : public TerminalPin
{
public:
    AnalogInputPin(const uint8_t& pin, const int& value = LOW) : TerminalPin(pin, value) {}

    virtual ~AnalogInputPin() = default;

    PinMode getMode() const override { return AnalogInput; }

    void setValue(const int& value) override
    {
        Pin::setValue(value);
        _mIsStale = true;
    }

    void refresh() override
    {
        analogRead(getPin());
        _mIsStale = false;
    }

protected:
    int _scaleValue(const int& value) override { return value; }
};
