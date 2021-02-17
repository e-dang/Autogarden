#pragma once

#include <pins/pins.hpp>

class IMultiplexerTranslationPolicy {
public:
    virtual ~IMultiplexerTranslationPolicy() = default;

    virtual bool translate(ILogicInputPinSet* inputPins, ILogicOutputPinSet* outputPins, ILogicInputPin* sigPin) = 0;
};