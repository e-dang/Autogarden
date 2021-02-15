#pragma once

#include <pins/interfaces/output.hpp>

class ITerminalPin : virtual public IOutputPin {
public:
    virtual ~ITerminalPin() = default;

    virtual void initialize() = 0;
};