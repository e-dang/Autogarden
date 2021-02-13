#pragma once

#include <initializer_list>
#include <pins/output_pin_set.hpp>
#include <pins/terminal_pin.hpp>

template <typename T>
class ITerminalPinSet : virtual public IOutputPinSet
{
    static_assert(std::is_base_of<ITerminalPin, T>::value, "Type T must implement the ITerminalPin interface");

public:
    virtual ~ITerminalPinSet() = default;

    virtual void refresh() = 0;
};

template <typename T>
class TerminalPinSet : public GenericOutputPinSet<T>, public ITerminalPinSet<T>
{
public:
    TerminalPinSet(std::vector<T>&& pins) : GenericOutputPinSet<T>(std::move(pins)) {}

    virtual ~TerminalPinSet() = default;

    void refresh() override
    {
        std::for_each(this->_mPins.begin(), this->_mPins.end(), [](T& pin) {
            if (pin.isStale())
                pin.refresh();
        });
    }
};

template <typename T>
TerminalPinSet<T>* createTerminalPinSet(const std::initializer_list<uint8_t>& pinNums)
{
    std::vector<T> pins;
    pins.reserve(pinNums.size());
    std::for_each(pinNums.begin(), pinNums.end(), [&pins](const uint8_t& pinNum) { pins.emplace_back(pinNum); });
    return new TerminalPinSet<T>(std::move(pins));
}