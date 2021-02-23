#pragma once

#include <pins/interfaces/pin.hpp>

class Pin : virtual public IPin {
public:
    Pin(const int& pinNum, const PinMode& pinMode) : __mPinNum(pinNum), __mPinMode(pinMode) {}

    virtual ~Pin() = default;

    int getPinNum() const override {
        return __mPinNum;
    }

    PinMode getMode() const override {
        return __mPinMode;
    }

private:
    int __mPinNum;
    PinMode __mPinMode;
};