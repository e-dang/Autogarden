#pragma once

#include <pins/output_pin_set.hpp>

class MultiplexerOutputPinSet : public OutputPinSet<IPin*> {
public:
    MultiplexerOutputPinSet(std::vector<IPin*>&& pins) : OutputPinSet<IPin*>(std::move(pins)) {}

    virtual ~MultiplexerOutputPinSet() = default;

protected:
    PinView _createPinView(IPin* pin) override {
        return PinView(pin, [this, pin]() { this->_resetPinsExcept(pin); });
    }

    void _resetPinsExcept(IPin* exceptionPin) {
        std::for_each(_mPins.begin(), _mPins.end(), [&exceptionPin](IPin* pin) {
            if (pin != exceptionPin) {
                pin->setValue(LOW);
            }
        });
    }
};