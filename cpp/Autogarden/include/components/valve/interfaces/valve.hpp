#pragma once

#include <components/di_state_actuator.hpp>

class IValve : public DiStateActuator {
public:
    IValve(const std::string& id, ILogicInputPin* inputPin, const int& onValue, const int& offValue) :
        DiStateActuator(id, inputPin, onValue, offValue) {}

    virtual ~IValve() = default;

    virtual bool open() = 0;

    virtual bool close() = 0;
};