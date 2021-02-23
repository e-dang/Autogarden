#pragma once

#include <pins/interfaces/output.hpp>
#include <pins/pin.hpp>

class OutputPin : public Pin, virtual public IOutputPin {
public:
    OutputPin(const int& pinNum, const PinMode& pinMode) : Pin(pinNum, pinMode), __mIsConnected(false) {}

    virtual ~OutputPin() = default;

    bool isConnected() const override {
        return __mIsConnected;
    }

    virtual void connect() override {
        __mIsConnected = true;
    }

    virtual void disconnect() override {
        __mIsConnected = false;
    }

private:
    bool __mIsConnected;
};