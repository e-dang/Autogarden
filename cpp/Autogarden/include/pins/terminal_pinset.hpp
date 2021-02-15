#pragma once

#include <pins/interfaces/terminal_pinset.hpp>
#include <pins/output_pinset.hpp>

class TerminalPinSet : public ITerminalPinSet, public OutputPinSet<ITerminalPin*> {
public:
    TerminalPinSet(std::vector<ITerminalPin*> pins) : OutputPinSet<ITerminalPin*>(pins) {}

    ITerminalPin* at(const int& idx) override {
        return __mPins[idx];
    };
};