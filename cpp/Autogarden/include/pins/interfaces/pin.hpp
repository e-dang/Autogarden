#pragma once

class ISignal;

enum PinMode { DigitalOutput, DigitalInput, AnalogOutput, AnalogInput, Undefined };

class IPin {
public:
    virtual ~IPin() = default;

    virtual void processSignal(ISignal* signal) = 0;

    virtual int getPinNum() = 0;

    virtual PinMode getMode() = 0;
};