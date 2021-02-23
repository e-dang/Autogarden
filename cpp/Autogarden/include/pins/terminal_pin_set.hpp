#pragma once

#include <initializer_list>
#include <pins/output_pin_set.hpp>
#include <pins/terminal_pin.hpp>

class ITerminalPinSet : virtual public IOutputPinSet {
public:
    virtual ~ITerminalPinSet() = default;

    virtual void refresh() = 0;
};

class TerminalPinSet : public OutputPinSet<ITerminalPin*>, public ITerminalPinSet {
public:
    TerminalPinSet(std::vector<ITerminalPin*>&& pins) : OutputPinSet<ITerminalPin*>(std::move(pins)) {}

    virtual ~TerminalPinSet() = default;

    void refresh() override {
        std::for_each(this->_mPins.begin(), this->_mPins.end(), [](ITerminalPin*& pin) {
            if (pin->isStale())
                pin->refresh();
        });
    }
};