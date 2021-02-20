#pragma once

#include <components/pump/interfaces/pump.hpp>

class Pump : public IPump {
public:
    Pump(const std::string& id, ILogicInputPin* inputPin, const int& onValue = HIGH, const int& offValue = LOW) :
        IPump(id, inputPin, onValue, offValue) {}

    bool start() override {
        return _performAction(_mOnValue);
    }

    bool stop() override {
        return _performAction(_mOffValue);
    }
};