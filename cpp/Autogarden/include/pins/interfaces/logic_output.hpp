#pragma once

#include <pins/interfaces/output.hpp>

class ILogicOutputPin : virtual public IOutputPin {
public:
    virtual ~ILogicOutputPin() = default;

    virtual std::shared_ptr<ISignal> popSignal() = 0;

    virtual bool hasSignal() const = 0;

    virtual int getSignalValue() const = 0;
};