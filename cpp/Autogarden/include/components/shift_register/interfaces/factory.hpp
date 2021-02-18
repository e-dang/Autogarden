#pragma once

#include <components/shift_register/interfaces/shift_register.hpp>
#include <memory>

class IShiftRegisterFactory {
public:
    virtual ~IShiftRegisterFactory() = default;

    virtual std::unique_ptr<IShiftRegister> create(const std::string& id, const int& numOutputPins,
                                                   const int& direction) = 0;
};