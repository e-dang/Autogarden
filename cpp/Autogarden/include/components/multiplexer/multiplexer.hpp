#pragma once

#include <components/multiplexer/interfaces/multiplexer.hpp>
#include <components/multiplexer/interfaces/translation_policy.hpp>
#include <vector>

class Multiplexer : public IMultiplexer {
public:
    Multiplexer(const std::string& id, ILogicInputPinSet* inputPins, ILogicOutputPinSet* outputPins,
                ILogicInputPin* sigPin, ILogicInputPin* enablePin, IMultiplexerTranslationPolicy* policy) :
        Component(id),
        __pInputPins(inputPins),
        __pOutputPins(outputPins),
        __pSigPin(sigPin),
        __pEnablePin(enablePin),
        __pPolicy(policy),
        __mIsEnabled(false) {}

    bool enable() override {
        return _setEnablePin(HIGH);
    }

    bool disable() override {
        return _setEnablePin(LOW);
    }

    bool isEnabled() override {
        return __mIsEnabled == true;
    }

    bool isDisabled() override {
        return __mIsEnabled == false;
    }

protected:
    bool _setInputPins(IOutputPinSet* outputPins) override {
        outputPins->connect(__pSigPin.get());
        outputPins->connect(__pEnablePin.get());
        outputPins->connect(__pInputPins.get());
        return true;
    }

    IOutputPinSet* _getOutputPins() override {
        return __pOutputPins.get();
    }

    bool _propagateSignal() override {
        disable();
        if (!__pPolicy->translate(__pInputPins.get(), __pOutputPins.get(), __pSigPin.get()))
            return false;

        enable();
        return Component::_propagateSignal();
    }

    bool _setEnablePin(const int& value) {
        if (__pEnablePin == nullptr)
            return false;

        DigitalWrite signal(value);
        if (__pEnablePin->processSignal(&signal)) {
            __mIsEnabled = static_cast<bool>(value);
            return true;
        }

        return false;
    }

private:
    bool __mIsEnabled;
    std::unique_ptr<ILogicInputPin> __pSigPin;
    std::unique_ptr<ILogicInputPin> __pEnablePin;
    std::unique_ptr<ILogicInputPinSet> __pInputPins;
    std::unique_ptr<ILogicOutputPinSet> __pOutputPins;
    std::unique_ptr<IMultiplexerTranslationPolicy> __pPolicy;
};