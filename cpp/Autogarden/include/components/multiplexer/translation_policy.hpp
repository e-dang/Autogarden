#pragma once

#include <components/multiplexer/interfaces/translation_policy.hpp>
#include <pins/pins.hpp>

class MultiplexerTranslationPolicy : public IMultiplexerTranslationPolicy {
public:
    ~MultiplexerTranslationPolicy() = default;

    bool translate(ILogicInputPinSet* inputPins, ILogicOutputPinSet* outputPins) override {
        const auto channel = __getChannelSignalFromInputs(outputPins);
        if (channel == MultiplexerTranslationPolicy::CHANNEL_NOT_SPECIFIED)
            return false;

        __translateChannelToInputSignals(channel, inputPins);
        __processInputSignals(inputPins);
        return true;
    }

    std::shared_ptr<ISignal> getSigPinSignal() override {
        return __pSigPinSignal;
    }

private:
    int __getChannelSignalFromInputs(ILogicOutputPinSet* outputPins) {
        for (int i = 0; i < outputPins->size(); i++) {
            auto pin = outputPins->at(i);
            if (pin->hasSignal()) {
                __pSigPinSignal = pin->popSignal();
                return i;
            }
        }

        return MultiplexerTranslationPolicy::CHANNEL_NOT_SPECIFIED;
    }

    void __translateChannelToInputSignals(const int& channel, ILogicInputPinSet* inputPins) {
        __mSignals.clear();
        for (int i = 0; i < inputPins->size(); i++) {
            __mSignals.emplace_back(std::make_shared<DigitalWrite>(__getBit(channel, i)));
        }
    }

    void __processInputSignals(ILogicInputPinSet* inputPins) {
        for (int i = 0; i < inputPins->size(); i++) {
            inputPins->at(i)->processSignal(__mSignals[i]);
        }
    }

    bool __getBit(const int& channel, const int& pos) {
        return static_cast<bool>(channel & (1 << pos));
    }

private:
    std::shared_ptr<ISignal> __pSigPinSignal;
    std::vector<std::shared_ptr<DigitalWrite>> __mSignals;

    static const int CHANNEL_NOT_SPECIFIED = -1;
};