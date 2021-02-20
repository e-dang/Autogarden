#pragma once

#include <components/pump/interfaces/factory.hpp>
#include <components/pump/pump.hpp>

class PumpFactory : public IPumpFactory {
public:
    std::unique_ptr<IPump> create(const std::string& id, const int& onValue = HIGH,
                                  const int& offValue = LOW) override {
        auto inputPin = __mInputPinSetFactory.createPin(0, PinMode::DigitalOutput);
        return std::make_unique<Pump>(id, inputPin.release(), onValue, offValue);
    }

private:
    PinFactory<LogicInputPinSet, LogicInputPin> __mInputPinSetFactory;
};