#pragma once

#include <pins/pins.hpp>

class IShiftRegisterInputPinSet : public ILogicInputPinSet {
public:
    virtual ~IShiftRegisterInputPinSet() = default;

    virtual bool openLatch() = 0;

    virtual bool closeLatch() = 0;

    virtual bool shiftOut(const int& binary) = 0;
};