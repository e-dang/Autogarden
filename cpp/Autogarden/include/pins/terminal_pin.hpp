#pragma once

#include <pins/pin.hpp>

class ITerminalPin : virtual public IPin
{
public:
    virtual ~ITerminalPin() = default;

    virtual bool isStale() const = 0;

    virtual void refresh() = 0;
};

class TerminalPin : public Pin, public ITerminalPin
{
public:
    TerminalPin(const uint8_t& pin, const int& value = LOW) : Pin(pin, value), _mIsStale(false) {}

    virtual ~TerminalPin() = default;

    bool isStale() const { return _mIsStale; }

    virtual void refresh() = 0;

protected:
    bool _mIsStale;
};
