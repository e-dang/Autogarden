#pragma once

#include <pins/interfaces/logic_input.hpp>

class ILogicInputPinSet {
public:
    typedef std::vector<ILogicInputPin*>::iterator iterator;

    virtual ~ILogicInputPinSet() = default;

    virtual iterator begin() = 0;

    virtual iterator end() = 0;

    virtual ILogicInputPin* at(const int& idx) = 0;

    virtual int size() const = 0;
};