#pragma once

#include <components/component.hpp>

class IShiftRegister : virtual public Component {
public:
    virtual ~IShiftRegister() = default;

    virtual bool enable() = 0;

    virtual bool disable() = 0;

    virtual bool isEnabled() = 0;

    virtual bool isDisabled() = 0;
};