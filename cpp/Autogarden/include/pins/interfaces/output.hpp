#pragma once

#include <pins/interfaces/pin.hpp>

class IOutputPin : virtual public IPin {
public:
    virtual ~IOutputPin() = default;

    virtual bool isConnected() = 0;

    virtual void setIsConnected(const bool& state) = 0;
};