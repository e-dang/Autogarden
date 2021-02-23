#pragma once

#include <pins/interfaces/terminal.hpp>

class ISignal {
public:
    virtual ~ISignal() = default;

    virtual bool execute(const ITerminalPin* pin) = 0;

    virtual int getValue() const = 0;
};