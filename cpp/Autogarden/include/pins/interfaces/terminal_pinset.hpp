#pragma once

#include <pins/interfaces/output_pinset.hpp>
#include <pins/interfaces/terminal.hpp>

class ITerminalPinSet : virtual public IOutputPinSet {
public:
    typedef std::vector<std::unique_ptr<ITerminalPin>>::iterator iterator;

    virtual ~ITerminalPinSet() = default;

    virtual ITerminalPin* at(const int& idx) = 0;

    virtual iterator begin() = 0;

    virtual iterator end() = 0;

    virtual void merge(std::unique_ptr<ITerminalPinSet>&& terminalPins) = 0;
};