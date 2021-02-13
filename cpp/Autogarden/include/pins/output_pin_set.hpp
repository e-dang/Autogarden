#pragma once

#include <pins/logic_pin.hpp>
#include <pins/pin_set.hpp>
#include <pins/pin_view.hpp>
#include <type_traits>
#include <utils.hpp>
#include <vector>

class IOutputPinSet : public PinSet
{
public:
    virtual ~IOutputPinSet() = default;

    virtual std::vector<PinView> getNextAvailable(const int& requestedNum, const PinMode& pinMode) = 0;

    virtual int getNumAvailable(const PinMode& pinMode) const = 0;

    virtual bool hasNumAvailable(const int& requestedNum, const PinMode& pinMode) const = 0;

    virtual std::vector<uint8_t> getPinNumbers() const = 0;

    virtual int getPinValue(const int& idx) const = 0;

protected:
    virtual PinView _createPinView(IPin* pin) = 0;
};

template <typename T>
class OutputPinSet : virtual public IOutputPinSet
{
public:
    OutputPinSet(std::vector<T>&& pins) : _mPins(std::move(pins)) {}

    virtual ~OutputPinSet() = default;

    std::vector<PinView> getNextAvailable(const int& requestedNum, const PinMode& pinMode) override
    {
        std::vector<PinView> pinViews;
        pinViews.reserve(requestedNum);
        for (int i = 0; i < size(); i++)
        {
            auto pin = _at(i);
            if (!pin->isConnected() && pin->getMode() == pinMode)
            {
                pinViews.push_back(_createPinView(pin));
                pin->setIsConnected(true);
                if (pinViews.size() == requestedNum)
                    break;
            }
        }

        return pinViews;
    }

    int getNumAvailable(const PinMode& pinMode) const override
    {
        return std::count_if(_mPins.cbegin(), _mPins.cend(), [&pinMode](const T& pin) {
            return !ptr(pin)->isConnected() && ptr(pin)->getMode() == pinMode;
        });
    }

    bool hasNumAvailable(const int& requestedNum, const PinMode& pinMode) const override
    {
        return requestedNum <= getNumAvailable(pinMode);
    }

    std::vector<uint8_t> getPinNumbers() const override
    {
        std::vector<uint8_t> pinNumbers;
        std::transform(_mPins.cbegin(), _mPins.cend(), std::back_inserter(pinNumbers),
                       [](const T& pin) { return ptr(pin)->getPin(); });
        return pinNumbers;
    }

    int size() const override { return static_cast<int>(_mPins.size()); }

    int getPinValue(const int& idx) const override { return _at(idx)->getValue(); }

protected:
    virtual PinView _createPinView(IPin* pin) override { return PinView(pin); }

    typename std::conditional<std::is_pointer<T>::value, const T, const T*>::type _at(const int& idx) const
    {
        return ptr(_mPins.at(idx));
    }

    typename std::conditional<std::is_pointer<T>::value, T, T*>::type _at(const int& idx)
    {
        return ptr(_mPins.at(idx));
    }

protected:
    std::vector<T> _mPins;
};