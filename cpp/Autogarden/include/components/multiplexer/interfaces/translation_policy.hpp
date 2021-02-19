#pragma once

#include <pins/pins.hpp>

class IMultiplexerTranslationPolicy {
public:
    virtual ~IMultiplexerTranslationPolicy() = default;

    virtual bool translate(ILogicInputPinSet* inputPins, ILogicOutputPinSet* outputPins) = 0;

    virtual std::shared_ptr<ISignal> getSigPinSignal() = 0;
};