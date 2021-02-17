#pragma once

#include <pins/interfaces/logic_input.hpp>
#include <pins/pin.hpp>

class LogicInputPin : public Pin, public ILogicInputPin {
public:
    LogicInputPin(const int& pinNum, const PinMode& pinMode) : Pin(pinNum, pinMode), __pOutputPin(nullptr) {}

    ~LogicInputPin() = default;

    bool processSignal(ISignal* signal) override {
        if (__pOutputPin == nullptr)
            return false;

        return __pOutputPin->processSignal(signal);
    }

    bool connect(IOutputPin* outputPin) override {
        if (outputPin->isConnected() || outputPin->getMode() != getMode())
            return false;

        __pOutputPin = outputPin;
        __pOutputPin->connect();
        return true;
    }

private:
    IOutputPin* __pOutputPin;
};