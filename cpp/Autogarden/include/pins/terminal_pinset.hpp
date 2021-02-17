#pragma once

#include <pins/interfaces/terminal_pinset.hpp>
#include <pins/output_pinset.hpp>

class TerminalPinSet : public ITerminalPinSet, public OutputPinSet<std::unique_ptr<ITerminalPin>> {
public:
    typedef ITerminalPin value_type;

    TerminalPinSet(std::vector<std::unique_ptr<ITerminalPin>>&& pins) :
        OutputPinSet<std::unique_ptr<ITerminalPin>>(std::move(pins)) {}

    ITerminalPin* at(const int& idx) override {
        return __mPins[idx].get();
    };
};