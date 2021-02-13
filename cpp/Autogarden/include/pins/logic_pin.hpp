#pragma once

#include <pins/pin.hpp>

class LogicPin : public Pin
{
public:
    LogicPin(const uint8_t& pin, const PinMode& pinMode, const int& value = LOW) : Pin(pin, value), __mPinMode(pinMode)
    {
    }

    virtual ~LogicPin() = default;

    PinMode getMode() const override { return __mPinMode; }

protected:
    int _scaleValue(const int& value) override { return value; }

private:
    PinMode __mPinMode;
};