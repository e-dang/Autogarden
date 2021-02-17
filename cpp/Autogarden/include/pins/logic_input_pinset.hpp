#pragma once

#include <pins/interfaces/logic_input_pinset.hpp>
#include <vector>

class LogicInputPinSet : public ILogicInputPinSet {
public:
    LogicInputPinSet(std::vector<std::unique_ptr<ILogicInputPin>>&& pins) : __mPins(std::move(pins)) {}

    virtual ~LogicInputPinSet() = default;

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
    std::vector<std::unique_ptr<ILogicInputPin>> __mPins;
};