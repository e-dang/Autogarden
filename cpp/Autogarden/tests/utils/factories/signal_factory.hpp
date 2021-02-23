#pragma once

#include <mocks/mock_signal.hpp>
#include <signals/signals.hpp>

class SignalMockFactory : public ISignalFactory {
public:
    std::shared_ptr<ISignal> createDigitalWriteSignal(const int& val) override {
        return std::make_shared<MockSignal>(val);
    }

    std::shared_ptr<ISignal> createDigitalReadSignal() override {
        return std::make_shared<MockSignal>();
    }

    std::shared_ptr<ISignal> createAnalogWriteSignal(const int& val) override {
        return std::make_shared<MockSignal>(val);
    }

    std::shared_ptr<ISignal> createAnalogReadSignal() override {
        return std::make_shared<MockSignal>();
    }

    template <typename T>
    T* getMockPtr(std::shared_ptr<ISignal> signal) {
        return dynamic_cast<T*>(signal.get());
    }
};