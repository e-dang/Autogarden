#pragma once

#include <initializer_list>
#include <pins/interfaces/pin.hpp>

template <typename T, typename U>
class IPinFactory {
public:
    virtual ~IPinFactory() = default;

    virtual std::unique_ptr<U> createPin(const int& pinNum, const PinMode& pinMode) = 0;

    virtual std::vector<std::unique_ptr<typename T::value_type>> createPinVector(
      const std::initializer_list<int>& pinNums, const PinMode& pinMode) = 0;

    virtual std::unique_ptr<T> createPinSet(
      std::vector<std::vector<std::unique_ptr<typename T::value_type>>>& pinVecs) = 0;

    virtual std::unique_ptr<T> createPinSet(const std::initializer_list<int>& pinNums, const PinMode& pinMode) = 0;

    virtual std::unique_ptr<T> createPinSet(const int& numPins, const PinMode& pinMode) = 0;
};