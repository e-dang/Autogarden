#pragma once

#include <pins/interfaces/output.hpp>

class ILogicOutputPin : virtual public IOutputPin {
public:
    virtual ~ILogicOutputPin() = default;

    virtual ISignal* popSignal() = 0;

    virtual bool hasSignal() const = 0;
};