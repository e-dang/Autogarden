#pragma once

#include <components/multiplexer/interfaces/translation_policy.hpp>
#include <pins/pins.hpp>

struct ChannelSignal {
    int channel;
    ISignal* signal;
};

class MultiplexerTranslationPolicy : public IMultiplexerTranslationPolicy {
public:
    ~MultiplexerTranslationPolicy() = default;

    bool translate(ILogicInputPinSet* inputPins, ILogicOutputPinSet* outputPins, ILogicInputPin* sigPin) override {
        const auto channelSignal = __getChannelSignalFromInputs(outputPins);
        if (channelSignal.channel == MultiplexerTranslationPolicy::CHANNEL_NOT_SPECIFIED)
            return false;

        sigPin->processSignal(channelSignal.signal);
        __translateChannelToInputSignals(channelSignal.channel, inputPins);
        __processInputSignals(inputPins);
        return true;
    }

private:
    ChannelSignal __getChannelSignalFromInputs(ILogicOutputPinSet* outputPins) {
        for (int i = 0; i < outputPins->size(); i++) {
            auto pin = outputPins->at(i);
            if (pin->hasSignal())
                return { i, pin->popSignal() };
        }

        return { MultiplexerTranslationPolicy::CHANNEL_NOT_SPECIFIED, nullptr };
    }

    void __translateChannelToInputSignals(const int& channel, ILogicInputPinSet* inputPins) {
        __mSignals.clear();
        for (int i = 0; i < inputPins->size(); i++) {
            __mSignals.emplace_back(__getBit(channel, i));
        }
    }

    void __processInputSignals(ILogicInputPinSet* inputPins) {
        for (int i = 0; i < inputPins->size(); i++) {
            inputPins->at(i)->processSignal(&__mSignals[i]);
        }
    }

    bool __getBit(const int& channel, const int& pos) {
        return static_cast<bool>(channel & (1 << pos));
    }

private:
    std::vector<DigitalWrite> __mSignals;

    static const int CHANNEL_NOT_SPECIFIED = -1;
};