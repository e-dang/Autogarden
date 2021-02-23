#pragma once

class ISignal;

enum PinMode { DigitalOutput, DigitalInput, AnalogOutput, AnalogInput, Count };

class IPin {
public:
    virtual ~IPin() = default;

    virtual bool processSignal(std::shared_ptr<ISignal> signal) = 0;

    virtual int getPinNum() const = 0;

    virtual PinMode getMode() const = 0;

    virtual bool isConnected() const = 0;

    virtual void disconnect() = 0;
};