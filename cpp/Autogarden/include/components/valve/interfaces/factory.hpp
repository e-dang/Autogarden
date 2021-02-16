#pragma once

#include <components/valve/interfaces/valve.hpp>
#include <memory>

class IValveFactory {
public:
    virtual ~IValveFactory() = default;

    virtual std::unique_ptr<IValve> create(const std::string& id, const int& onValue = HIGH,
                                           const int& offValue = LOW) = 0;
};