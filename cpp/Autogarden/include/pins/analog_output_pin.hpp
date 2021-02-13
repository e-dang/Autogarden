#pragma once

#include <Arduino.h>

#include <pins/terminal_pin.hpp>

class AnalogOutputPin : public TerminalPin
{
public:
    AnalogOutputPin(const uint8_t& pin, const int& value = LOW) : TerminalPin(pin, value) {}

    virtual ~AnalogOutputPin() = default;

    PinMode getMode() const override { return AnalogOutput; }

    void setValue(const int& value) override
    {
        Pin::setValue(value);
        _mIsStale = true;
    }

    void refresh() override
    {
        analogWrite(getPin(), getValue());
        _mIsStale = false;
    }

protected:
    int _scaleValue(const int& value) override
    {
        if (value > 255)
            return 255;
        else if (value < 0)
            return 0;
        else
            return value;
    }
};