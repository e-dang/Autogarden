#pragma once

#include <pins/pin.hpp>

class PinSet
{
public:
    virtual ~PinSet() = default;

    virtual PinMode getMode() const = 0;

    virtual int size() const = 0;
};