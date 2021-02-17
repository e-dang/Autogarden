#pragma once

#include <components/multiplexer/interfaces/factory.hpp>
#include <components/multiplexer/multiplexer.hpp>
#include <components/multiplexer/translation_policy.hpp>
#include <pins/pins.hpp>

class MultiplexerFactory : public IMultiplexerFactory {
public:
    std::unique_ptr<IMultiplexer> create(const std::string& id, const int& numLogicInputs, const int& numOutputs,
                                         const PinMode& sigMode) override {
        auto sigPin     = __mInputPinSetFactory.createPin(1, sigMode);
        auto enablePin  = __mInputPinSetFactory.createPin(1, PinMode::DigitalOutput);
        auto inputPins  = __mInputPinSetFactory.createPinSet(numLogicInputs, PinMode::DigitalOutput);
        auto outputPins = __mOutputPinSetFactory.createPinSet(numOutputs, sigMode);
        auto policy     = new MultiplexerTranslationPolicy();
        return std::make_unique<Multiplexer>(id, inputPins.release(), outputPins.release(), sigPin.release(),
                                             enablePin.release(), policy);
    }

private:
    PinFactory<LogicInputPinSet, LogicInputPin> __mInputPinSetFactory;
    PinFactory<LogicOutputPinSet, LogicOutputPin> __mOutputPinSetFactory;
};