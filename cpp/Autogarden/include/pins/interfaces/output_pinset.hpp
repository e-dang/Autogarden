#pragma once

#include <pins/interfaces/logic_input_pinset.hpp>

class IOutputPinSet {
public:
    virtual bool connect(ILogicInputPinSet* inputPins) = 0;

    virtual bool connect(ILogicInputPin* inputPin) = 0;

    virtual int size() const = 0;
};