#pragma once
#include <pins/pins.hpp>

class IOutputToInputPolicy {
public:
    virtual ~IOutputToInputPolicy() = default;

    virtual bool execute(IInputPinSet* inputPins, const IOutputPinSet* outputPins) = 0;
};

class MultiplexerOIPolicy : public IOutputToInputPolicy {
public:
    ~MultiplexerOIPolicy() = default;

    bool execute(IInputPinSet* inputPins, const IOutputPinSet* outputPins) override {
        if (inputPins == nullptr || outputPins == nullptr)
            return false;

        auto channel = __calcChannelFromOutput(outputPins);
        if (channel == CHANNEL_NOT_SPECIFIED)
            return false;

        __translateChannelToInputs(inputPins, channel);
        return true;
    }

private:
    int __calcChannelFromOutput(const IOutputPinSet* outputPins) {
        for (int i = 0; i < outputPins->size(); i++) {
            if (outputPins->getPinValue(i) >= HIGH) {
                return i;
            }
        }

        return CHANNEL_NOT_SPECIFIED;
    }

    void __translateChannelToInputs(IInputPinSet* inputPins, const int& channel) {
        for (int i = 0; i < inputPins->size(); i++) {
            inputPins->setPin(i, __getBit(channel, i));
        }
    }

    bool __getBit(const int& num, const int& pos) {
        return static_cast<bool>(num & (1 << pos));
    }

private:
    static const int CHANNEL_NOT_SPECIFIED = -1;
};