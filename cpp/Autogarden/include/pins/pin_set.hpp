#pragma once

#include <pins/pin.hpp>

class PinSet
{
public:
    virtual ~PinSet() = default;

    virtual int size() const = 0;
};