#pragma once

#include <pins/interfaces/logic_output.hpp>
#include <pins/output.hpp>

class LogicOutputPin : public OutputPin, public ILogicOutputPin {
public:
    LogicOutputPin(const int& pinNum, const PinMode& pinMode) : OutputPin(pinNum, pinMode), __pSignal(nullptr) {}

    ~LogicOutputPin() = default;

    void processSignal(ISignal* signal) override {
        __pSignal = signal;
    }

    ISignal* popSignal() override {
        auto signal = __pSignal;
        __pSignal   = nullptr;
        return signal;
    }

    bool hasSignal() const override {
        return __pSignal != nullptr;
    }

private:
    ISignal* __pSignal;
};