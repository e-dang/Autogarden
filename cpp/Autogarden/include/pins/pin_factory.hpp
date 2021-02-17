#pragma once

#include <pins/interfaces/pin_factory.hpp>

template <typename T, typename U>
class PinFactory : IPinFactory<T, U> {
public:
    std::unique_ptr<U> createPin(const int& pinNum, const PinMode& pinMode) override {
        return std::make_unique<U>(pinNum, pinMode);
    }

    std::vector<std::unique_ptr<typename T::value_type>> createPinVector(const std::initializer_list<int>& pinNums,
                                                                         const PinMode& pinMode) override {
        std::vector<std::unique_ptr<typename T::value_type>> pins;
        pins.reserve(pinNums.size());
        for (const auto& pinNum : pinNums) {
            pins.emplace_back(createPin(pinNum, pinMode));
        }
        return pins;
    }

    std::unique_ptr<T> createPinSet(
      std::vector<std::vector<std::unique_ptr<typename T::value_type>>>& pinVecs) override {
        std::vector<std::unique_ptr<typename T::value_type>> pins;

        auto size = 0;
        for (auto& pinVec : pinVecs) {
            size += pinVec.size();
        }

        pins.reserve(size);

        for (auto& pinVec : pinVecs) {
            std::move(pinVec.begin(), pinVec.end(), std::back_inserter(pins));
        }

        return std::make_unique<T>(std::move(pins));
    }

    std::unique_ptr<T> createPinSet(const std::initializer_list<int>& pinNums, const PinMode& pinMode) override {
        std::vector<std::unique_ptr<typename T::value_type>> pins;
        pins.reserve(pinNums.size());
        for (const auto& pinNum : pinNums) {
            pins.emplace_back(createPin(pinNum, pinMode));
        }
        return std::make_unique<T>(std::move(pins));
    }

    std::unique_ptr<T> createPinSet(const int& numPins, const PinMode& pinMode) override {
        std::vector<std::unique_ptr<typename T::value_type>> pins;
        pins.reserve(numPins);
        for (int i = 0; i < numPins; i++) {
            pins.emplace_back(createPin(i, pinMode));
        }
        return std::make_unique<T>(std::move(pins));
    }
};