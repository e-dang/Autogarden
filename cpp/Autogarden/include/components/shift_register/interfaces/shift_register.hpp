#pragma once

#include <components/component.hpp>

class IShiftRegister : public Component {
public:
    IShiftRegister(const std::string& id) : Component(id) {}

    virtual ~IShiftRegister() = default;
};