#pragma once

#include <pins/logic_pin.hpp>
#include <pins/pin_set.hpp>
#include <pins/pin_view.hpp>
#include <type_traits>
#include <vector>

class IOutputPinSet : public PinSet
{
public:
    virtual ~IOutputPinSet() = default;

    virtual std::vector<PinView> getNextAvailable(const int& requestedNum) = 0;

    virtual int getNumAvailable() const = 0;

    virtual std::vector<uint8_t> getPinNumbers() const = 0;
};

template <typename T>
class GenericOutputPinSet : virtual public IOutputPinSet
{
public:
    GenericOutputPinSet(std::vector<T>&& pins) : _mPins(std::move(pins)) {}

    virtual ~GenericOutputPinSet() = default;

    std::vector<PinView> getNextAvailable(const int& requestedNum) override
    {
        std::vector<PinView> pinViews;
        pinViews.reserve(requestedNum);
        for (int i = 0; i < size(); i++)
        {
            auto& pin = _mPins[i];
            if (!pin.isConnected())
            {
                pinViews.push_back(PinView(&pin));
                pin.setIsConnected(true);
                if (pinViews.size() == requestedNum)
                    break;
            }
        }

        return pinViews;
    }

    int getNumAvailable() const override
    {
        return std::count_if(_mPins.cbegin(), _mPins.cend(), [](const T& pin) { return !pin.isConnected(); });
    }

    std::vector<uint8_t> getPinNumbers() const override
    {
        std::vector<uint8_t> pinNumbers;
        std::transform(_mPins.cbegin(), _mPins.cend(), std::back_inserter(pinNumbers),
                       [](const T& pin) { return pin.getPin(); });
        return pinNumbers;
    }

    PinMode getMode() const override { return _mPins[0].getMode(); }

    int size() const override { return static_cast<int>(_mPins.size()); }

protected:
    std::vector<T> _mPins;
};

// template <typename T>
// T* ptr(T& obj)
// {
//     return &obj;
// }

// template <typename T>
// T* ptr(T* obj)
// {
//     return obj;
// }

class OutputPinSet
{
public:
    OutputPinSet(const int& numPins, const PinMode& pinMode) : __mPins(numPins, nullptr)
    {
        for (int i = 0; i < size(); i++)
        {
            __mPins[i] = new LogicPin(i, pinMode);
        }
    }

    virtual ~OutputPinSet() = default;

    PinMode getMode() const { return __mPins[0]->getMode(); }

    int size() const { return static_cast<int>(__mPins.size()); }

    bool hasNumAvailable(const int& requestedNum, const PinMode& pinMode) const
    {
        return requestedNum <=
                 std::count_if(__mPins.cbegin(), __mPins.cend(),
                               [](const decltype(__mPins)::value_type& pin) { return !pin->isConnected(); }) &&
               pinMode == getMode();
    }

    std::vector<PinView> getNextAvailable(const int& requestedNum, const PinMode& pinMode)
    {
        std::vector<PinView> pinViews;
        pinViews.reserve(requestedNum);
        for (int i = 0; i < size(); i++)
        {
            auto pin = __mPins[i];
            if (!pin->isConnected())
            {
                pinViews.push_back(createPinView(pin));
                pin->setIsConnected(true);
                if (pinViews.size() == requestedNum)
                    break;
            }
        }

        return pinViews;
    }

    int getPinValue(const int& idx) const
    {
        if (idx < size() && idx >= 0)
        {
            return __mPins[idx]->getValue();
        }

        return INT32_MIN;
    }

protected:
    virtual PinView createPinView(Pin* pin) { return PinView(pin); }

protected:
    std::vector<Pin*> __mPins;
};
