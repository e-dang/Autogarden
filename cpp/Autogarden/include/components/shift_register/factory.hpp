#pragma once

#include <components/shift_register/input_pinset.hpp>
#include <components/shift_register/interfaces/factory.hpp>
#include <components/shift_register/shift_register.hpp>

class ShiftRegisterFactory : public IShiftRegisterFactory {
public:
    std::unique_ptr<IShiftRegister> create(const std::string& id, const int& numOutputPins,
                                           const int& direction) override {
        auto logicPin = __mInputPinFactory.createPin(0, PinMode::DigitalOutput);
        auto dataPin  = __mInputPinFactory.createPin(1, PinMode::DigitalOutput);
        auto clockPin = __mInputPinFactory.createPin(2, PinMode::DigitalOutput);
        auto inputPinSet =
          new ShiftRegisterInputPinSet(logicPin.release(), dataPin.release(), clockPin.release(), direction);
        auto outputPinSet = __mOutputPinFactory.createPinSet(numOutputPins, PinMode::DigitalOutput);
        return std::make_unique<ShiftRegister>(id, inputPinSet, outputPinSet.release());
    }

private:
    PinFactory<LogicInputPinSet, LogicInputPin> __mInputPinFactory;
    PinFactory<LogicOutputPinSet, LogicOutputPin> __mOutputPinFactory;
};