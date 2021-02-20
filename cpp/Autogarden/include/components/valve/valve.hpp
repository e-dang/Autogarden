#pragma once

#include <components/valve/interfaces/valve.hpp>

class Valve : public IValve {
public:
    Valve(const std::string& id, ILogicInputPin* inputPin, const int& onValue = HIGH, const int& offValue = LOW) :
        IValve(id, inputPin, onValue, offValue) {}

    bool open() override {
        return _performAction(_mOnValue);
    }

    bool close() override {
        return _performAction(_mOffValue);
    }
};