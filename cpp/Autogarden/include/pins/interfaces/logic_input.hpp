#pragma once

#include <pins/interfaces/output.hpp>

class ILogicInputPin : virtual public IPin {
public:
    virtual ~ILogicInputPin() = default;

    virtual bool connect(IOutputPin* outputPin) = 0;
};