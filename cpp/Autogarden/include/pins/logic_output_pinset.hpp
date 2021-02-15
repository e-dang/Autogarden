#pragma once

#include <pins/interfaces/logic_output_pinset.hpp>
#include <pins/output_pinset.hpp>
// #include <vector>

class LogicOutputPinSet : public ILogicOutputPinSet, public OutputPinSet<ILogicOutputPin*> {
public:
    LogicOutputPinSet(std::vector<ILogicOutputPin*> pins) : OutputPinSet<ILogicOutputPin*>(pins) {}

    ILogicOutputPin* at(const int& idx) override {
        return __mPins[idx];
    };
};