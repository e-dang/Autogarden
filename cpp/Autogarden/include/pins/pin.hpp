#pragma once

#include <stdint.h>

enum PinMode
{
    Digital,
    AnalogInput,
    AnalogOutput
};

class IPin
{
public:
    virtual ~IPin() = default;

    virtual uint8_t getPin() const = 0;

    virtual bool isConnected() const = 0;

    virtual void setIsConnected(const bool& value) = 0;

    virtual int getValue() const = 0;

    virtual void setValue(const int& value) = 0;

    virtual PinMode getMode() const = 0;

protected:
    virtual int _scaleValue(const int& value) = 0;
};

class Pin : virtual public IPin
{
public:
    Pin(const uint8_t& pin, const int& value = LOW) : __mValue(value), __mPin(pin), __mIsConnected(false) {}

    uint8_t getPin() const { return __mPin; }

    bool isConnected() const { return __mIsConnected; }

    void setIsConnected(const bool& value) { __mIsConnected = value; }

    int getValue() const { return __mValue; }

    virtual void setValue(const int& value) { __mValue = _scaleValue(value); }

private:
    int __mValue;
    uint8_t __mPin;
    bool __mIsConnected;
};