#pragma once

#include <components/component.hpp>

class IShiftRegister : public Component {
public:
    IShiftRegister(const String& id) : Component(id) {}

    virtual ~IShiftRegister() = default;
};