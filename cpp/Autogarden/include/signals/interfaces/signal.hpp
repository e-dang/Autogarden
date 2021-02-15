#pragma once

#include <pins/interfaces/terminal.hpp>

class ISignal {
public:
    virtual ~ISignal() = default;

    virtual void execute(const ITerminalPin* pin) = 0;
};