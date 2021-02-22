#pragma once

#include <pins/interfaces/terminal_pinset.hpp>
#include <pins/output_pinset.hpp>

class TerminalPinSet : public ITerminalPinSet, public OutputPinSet<std::unique_ptr<ITerminalPin>> {
public:
    TerminalPinSet(std::vector<std::unique_ptr<ITerminalPin>>&& pins) :
        OutputPinSet<std::unique_ptr<ITerminalPin>>(std::move(pins)) {}

    ITerminalPin* at(const int& idx) override {
        return __mPins[idx].get();
    };

    iterator begin() override {
        return __mPins.begin();
    }

    iterator end() override {
        return __mPins.end();
    }

    void merge(std::unique_ptr<ITerminalPinSet>&& terminalPins) override {
        __mPins.reserve(size() + terminalPins->size());
        std::move(terminalPins->begin(), terminalPins->end(), std::back_inserter(__mPins));
    }
};