#pragma once

#include <components/component.hpp>

class IShiftRegister : public Component {
public:
    IShiftRegister(const std::string& id) : Component(id) {}

    virtual ~IShiftRegister() = default;

    virtual bool enable() = 0;

    virtual bool disable() = 0;

    virtual bool isEnabled() = 0;

    virtual bool isDisabled() = 0;
};