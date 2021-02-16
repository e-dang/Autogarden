#pragma once

#include <pins/interfaces/logic_output.hpp>
#include <pins/interfaces/output_pinset.hpp>

class ILogicOutputPinSet : virtual public IOutputPinSet {
public:
    virtual ~ILogicOutputPinSet() = default;

    virtual ILogicOutputPin* at(const int& idx) = 0;
};