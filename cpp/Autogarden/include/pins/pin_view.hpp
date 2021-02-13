#pragma once

#include <functional>
#include <pins/pin.hpp>

struct PinView
{
    std::function<void(int)> set;
    std::function<uint8_t(void)> getPin;
    bool isNull;

    PinView(IPin* pin) :
        set([pin](const int& value) { pin->setValue(value); }),
        getPin([pin]() { return pin->getPin(); }),
        isNull(pin == nullptr)
    {
    }

    PinView(IPin* pin, const std::function<void(void)>& setterCallback) :
        set([pin, setterCallback](const int& value) {
            pin->setValue(value);
            setterCallback();
        }),
        getPin([pin]() { return pin->getPin(); }),
        isNull(pin == nullptr)
    {
    }
};