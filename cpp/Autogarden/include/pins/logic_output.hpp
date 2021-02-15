#pragma once

#include <pins/interfaces/logic_output.hpp>
#include <pins/output.hpp>

class LogicOutputPin : public OutputPin, public ILogicOutputPin {
public:
    LogicOutputPin(const int& pinNum, const PinMode& pinMode) : OutputPin(pinNum, pinMode), __mSignal(nullptr) {}

    ~LogicOutputPin() = default;

    void processSignal(ISignal* signal) override {
        __mSignal = signal;
    }

    ISignal* popSignal() override {
        auto signal = __mSignal;
        __mSignal   = nullptr;
        return signal;
    }

    bool hasSignal() const override {
        return __mSignal != nullptr;
    }

private:
    ISignal* __mSignal;
};