#pragma once

#include <components/valve/interfaces/factory.hpp>
#include <components/valve/valve.hpp>

class ValveFactory : public IValveFactory {
public:
    std::unique_ptr<IValve> create(const std::string& id, const int& onValue = HIGH,
                                   const int& offValue = LOW) override {
        return std::make_unique<Valve>(id, new LogicInputPin(0, PinMode::DigitalOutput), onValue, offValue);
    }
};