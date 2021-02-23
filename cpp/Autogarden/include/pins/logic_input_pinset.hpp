#pragma once

#include <pins/interfaces/logic_input_pinset.hpp>
#include <vector>

class LogicInputPinSet : public ILogicInputPinSet {
public:
    typedef ILogicInputPin value_type;

    LogicInputPinSet(std::vector<std::unique_ptr<ILogicInputPin>>&& pins) : __mPins(std::move(pins)) {}

    virtual ~LogicInputPinSet() = default;

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
    std::vector<std::unique_ptr<ILogicInputPin>> __mPins;
};