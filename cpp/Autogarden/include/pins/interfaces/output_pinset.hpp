#pragma once

#include <pins/interfaces/logic_input_pinset.hpp>

class IOutputPinSet {
public:
    virtual void connect(ILogicInputPinSet* inputPins) = 0;

    virtual void connect(ILogicInputPin* inputPin) = 0;

    virtual int size() const = 0;
};