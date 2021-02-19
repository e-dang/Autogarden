#pragma once

#include <pins/interfaces/logic_output.hpp>
#include <pins/output.hpp>
#include <signals/signals.hpp>

class LogicOutputPin : public OutputPin, public ILogicOutputPin {
public:
    LogicOutputPin(const int& pinNum, const PinMode& pinMode) : OutputPin(pinNum, pinMode), __pSignal(nullptr) {}

    ~LogicOutputPin() = default;

    bool processSignal(std::shared_ptr<ISignal> signal) override {
        __pSignal = signal;
        return true;
    }

    std::shared_ptr<ISignal> popSignal() override {
        auto signal = __pSignal;
        __pSignal   = nullptr;
        return signal;
    }

    bool hasSignal() const override {
        return __pSignal.get() != nullptr;
    }

    int getSignalValue() const override {
        return __pSignal->getValue();
    }

private:
    std::shared_ptr<ISignal> __pSignal;
};