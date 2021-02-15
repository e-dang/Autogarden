#pragma once

#include <pins/interfaces/pin.hpp>

class IOutputPin : virtual public IPin {
public:
    virtual ~IOutputPin() = default;

    virtual bool isConnected() const = 0;

    virtual void connect() = 0;

    virtual void disconnect() = 0;
};