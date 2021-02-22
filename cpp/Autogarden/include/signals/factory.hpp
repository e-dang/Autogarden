#pragma once

#include <signals/analog_read.hpp>
#include <signals/analog_write.hpp>
#include <signals/digital_read.hpp>
#include <signals/digital_write.hpp>

class ISignalFactory {
public:
    virtual ~ISignalFactory() = default;

    virtual std::shared_ptr<ISignal> createDigitalWriteSignal(const int& val) = 0;

    virtual std::shared_ptr<ISignal> createDigitalReadSignal() = 0;

    virtual std::shared_ptr<ISignal> createAnalogWriteSignal(const int& val) = 0;

    virtual std::shared_ptr<ISignal> createAnalogReadSignal() = 0;
};

class SignalFactory : public ISignalFactory {
public:
    std::shared_ptr<ISignal> createDigitalWriteSignal(const int& val) override {
        return std::make_shared<DigitalWrite>(val);
    }

    std::shared_ptr<ISignal> createDigitalReadSignal() override {
        return std::make_shared<DigitalRead>();
    }

    std::shared_ptr<ISignal> createAnalogWriteSignal(const int& val) override {
        return std::make_shared<AnalogWrite>(val);
    }

    std::shared_ptr<ISignal> createAnalogReadSignal() override {
        return std::make_shared<AnalogRead>();
    }
};