#pragma once

class ISignal;

enum PinMode { DigitalOutput, DigitalInput, AnalogOutput, AnalogInput, Undefined };

class IPin {
public:
    virtual ~IPin() = default;

    virtual void processSignal(ISignal* signal) const = 0;

    virtual int getPinNum() const = 0;

    virtual PinMode getMode() const = 0;
};