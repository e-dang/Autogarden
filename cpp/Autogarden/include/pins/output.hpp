#pragma once

#include <pins/interfaces/output.hpp>
#include <pins/pin.hpp>

class OutputPin : public Pin, virtual public IOutputPin {
public:
    OutputPin(const int& pinNum, const PinMode& pinMode) : Pin(pinNum, pinMode) {}

    virtual ~OutputPin() = default;

    bool isConnected() override {
        return __mIsConnected;
    }

    void setIsConnected(const bool& state) override {
        __mIsConnected = state;
    }

private:
    bool __mIsConnected;
};