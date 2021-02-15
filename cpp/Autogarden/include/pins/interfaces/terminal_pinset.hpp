#pragma once

#include <pins/interfaces/output_pinset.hpp>
#include <pins/interfaces/terminal.hpp>

class ITerminalPinSet : virtual public IOutputPinSet {
public:
    virtual ITerminalPin* at(const int& idx) = 0;
};