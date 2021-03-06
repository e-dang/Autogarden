#pragma once

#include <components/multiplexer/interfaces/multiplexer.hpp>
#include <components/multiplexer/interfaces/translation_policy.hpp>
#include <vector>

class Multiplexer : public IMultiplexer {
public:
    Multiplexer(const String& id, ILogicInputPinSet* inputPins, ILogicOutputPinSet* outputPins, ILogicInputPin* sigPin,
                ILogicInputPin* enablePin, IMultiplexerTranslationPolicy* policy) :
        IMultiplexer(id),
        __pInputPins(inputPins),
        __pOutputPins(outputPins),
        __pSigPin(sigPin),
        __pEnablePin(enablePin),
        __pPolicy(policy),
        __mIsDisabled(true) {}

    bool enable() override {
        return _setEnablePin(LOW);
    }

    bool disable() override {
        return _setEnablePin(HIGH);
    }

    bool isEnabled() override {
        return __mIsDisabled == false;
    }

    bool isDisabled() override {
        return __mIsDisabled == true;
    }

protected:
    bool _setInputPins(Component* parent) override {
        auto rootOutputPins   = _getComponentOutputPins(parent->getRoot());
        auto parentOutputPins = _getComponentOutputPins(parent);
        if (rootOutputPins == nullptr || parentOutputPins == nullptr)
            return false;

        if (!(rootOutputPins->connect(__pSigPin.get()) && rootOutputPins->connect(__pEnablePin.get()) &&
              parentOutputPins->connect(__pInputPins.get()))) {
            __pSigPin->disconnect();
            __pEnablePin->disconnect();
            __pInputPins->disconnect();
            return false;
        }

        return true;
    }

    IOutputPinSet* _getOutputPins() override {
        return __pOutputPins.get();
    }

    bool _propagateSignal() override {
        disable();
        if (!__pPolicy->translate(__pInputPins.get(), __pOutputPins.get()) || !Component::_propagateSignal())
            return false;

        enable();
        return __pSigPin->processSignal(__pPolicy->getSigPinSignal());  // sigPin must process signal as last operation
    }

    bool _setEnablePin(const int& value) {
        if (__pEnablePin == nullptr || !__pEnablePin->processSignal(std::make_shared<DigitalWrite>(value)))
            return false;

        __mIsDisabled = static_cast<bool>(value);
        return true;
    }

private:
    bool __mIsDisabled;
    std::unique_ptr<ILogicInputPin> __pSigPin;
    std::unique_ptr<ILogicInputPin> __pEnablePin;
    std::unique_ptr<ILogicInputPinSet> __pInputPins;
    std::unique_ptr<ILogicOutputPinSet> __pOutputPins;
    std::unique_ptr<IMultiplexerTranslationPolicy> __pPolicy;
};