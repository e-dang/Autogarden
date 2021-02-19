#pragma once

#include <components/shift_register/input_pinset.hpp>
#include <components/shift_register/interfaces/shift_register.hpp>

class ShiftRegister : public IShiftRegister {
public:
    ShiftRegister(const std::string& id, IShiftRegisterInputPinSet* inputPins, ILogicOutputPinSet* outputPins) :
        IShiftRegister(id), __pInputPins(inputPins), __pOutputPins(outputPins) {}

    bool enable() override {
        return true;
    }

    bool disable() override {
        return true;
    }

    bool isEnabled() override {
        return true;
    }

    bool isDisabled() override {
        return true;
    }

protected:
    bool _setInputPins(Component* parent) override {
        auto parentOutputPins = _getComponentOutputPins(parent);
        if (parentOutputPins == nullptr)
            return false;

        return parentOutputPins->connect(__pInputPins.get());
    }

    IOutputPinSet* _getOutputPins() override {
        return __pOutputPins.get();
    }

    bool _propagateSignal() override {
        disable();

        auto binary = __translateOutputsToBinary();
        __pInputPins->openLatch();
        __pInputPins->shiftOut(binary);
        __pInputPins->closeLatch();

        enable();
        return Component::_propagateSignal();
    }

private:
    int __translateOutputsToBinary() {
        int binNum = 0;
        for (int i = 0; i < __pOutputPins->size(); i++) {
            auto pin = __pOutputPins->at(i);
            if (pin->hasSignal() && pin->getSignalValue() == HIGH)
                binNum = __setBit(binNum, i);
        }

        return binNum;
    }

    int __setBit(const int& binNum, const int& pos) {
        return binNum | (1 << pos);
    }

private:
    std::unique_ptr<IShiftRegisterInputPinSet> __pInputPins;
    std::unique_ptr<ILogicOutputPinSet> __pOutputPins;
};