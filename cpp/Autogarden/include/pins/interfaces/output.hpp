#pragma once

#include <pins/interfaces/pin.hpp>

class IOutputPin : virtual public IPin {
public:
    virtual ~IOutputPin() = default;

    virtual void connect() = 0;
};