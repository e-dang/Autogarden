#pragma once

#include <pins/interfaces/logic_input.hpp>
#include <pins/pin.hpp>

class LogicInputPin : public Pin, public ILogicInputPin {
public:
    LogicInputPin(const int& pinNum, const PinMode& pinMode) : Pin(pinNum, pinMode), __pOutputPin(nullptr) {}

    ~LogicInputPin() = default;

    bool processSignal(std::shared_ptr<ISignal> signal) override {
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

    const IOutputPin* getOutputPin() const override {
        return __pOutputPin;
    }

    bool isConnected() const override {
        return __pOutputPin != nullptr;
    }

    void disconnect() override {
        if (isConnected()) {
            __pOutputPin->disconnect();
            __pOutputPin = nullptr;
        }
    }

private:
    IOutputPin* __pOutputPin;
};