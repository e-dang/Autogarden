#pragma once

#include <pins/interfaces/logic_output_pinset.hpp>
#include <pins/output_pinset.hpp>
// #include <vector>

class LogicOutputPinSet : public ILogicOutputPinSet, public OutputPinSet<std::unique_ptr<ILogicOutputPin>> {
public:
    LogicOutputPinSet(std::vector<std::unique_ptr<ILogicOutputPin>>&& pins) :
        OutputPinSet<std::unique_ptr<ILogicOutputPin>>(std::move(pins)) {}

    ILogicOutputPin* at(const int& idx) override {
        return __mPins[idx].get();
    };
};