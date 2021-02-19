#pragma once

#include <Arduino.h>

#include <components/shift_register/interfaces/input_pinset.hpp>

class ShiftRegisterInputPinSet : public IShiftRegisterInputPinSet {
public:
    ShiftRegisterInputPinSet(ILogicInputPin* latchPin, ILogicInputPin* dataPin, ILogicInputPin* clockPin,
                             const int& direction) :
        __pLatchPin(latchPin), __pDataPin(dataPin), __pClockPin(clockPin), __mPins(0), __mDirection(direction) {
        __mPins.emplace_back(latchPin);
        __mPins.emplace_back(dataPin);
        __mPins.emplace_back(clockPin);
    }

    bool openLatch() override {
        return __pLatchPin->processSignal(std::make_shared<DigitalWrite>(LOW));
    }

    bool closeLatch() override {
        return __pLatchPin->processSignal(std::make_shared<DigitalWrite>(HIGH));
    }

    bool shiftOut(const int& binary) override {
        auto dataPin  = __pDataPin->getOutputPin();
        auto clockPin = __pClockPin->getOutputPin();
        if (dataPin == nullptr || clockPin == nullptr)
            return false;

        ::shiftOut(dataPin->getPinNum(), clockPin->getPinNum(), __mDirection, binary);
        return true;
    }

    void disconnect() override {
        for (auto& pin : __mPins) {
            pin->disconnect();
        }
    }

    iterator begin() override {
        return __mPins.begin();
    }

    iterator end() override {
        return __mPins.end();
    }

    ILogicInputPin* at(const int& idx) override {
        return __mPins[idx].get();
    }

    int size() const override {
        return static_cast<int>(__mPins.size());
    }

private:
    int __mDirection;
    ILogicInputPin* __pLatchPin;
    ILogicInputPin* __pDataPin;
    ILogicInputPin* __pClockPin;
    std::vector<std::unique_ptr<ILogicInputPin>> __mPins;
};