#pragma once

#include <components/di_state_actuator.hpp>

class IPump : public DiStateActuator {
public:
    IPump(const std::string& id, ILogicInputPin* inputPin, const int& onValue, const int& offValue) :
        DiStateActuator(id, inputPin, onValue, offValue) {}

    virtual ~IPump() = default;

    virtual bool start() = 0;

    virtual bool stop() = 0;
};