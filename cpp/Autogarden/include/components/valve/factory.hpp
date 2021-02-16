#pragma once

#include <components/valve/interfaces/factory.hpp>
#include <components/valve/valve.hpp>

class ValveFactory : public IValveFactory {
public:
    std::unique_ptr<IValve> createValve(const std::string& id, const int& onValue = HIGH, const int& offValue = LOW) {
        return std::make_unique<Valve>(id, onValue, offValue);
    }
};