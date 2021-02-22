#pragma once

#include <mocks/mock_logic_input.hpp>
#include <mocks/mock_logic_input_pinset.hpp>
#include <mocks/mock_logic_output.hpp>
#include <mocks/mock_logic_output_pinset.hpp>
#include <mocks/mock_output.hpp>
#include <mocks/mock_terminal.hpp>
#include <mocks/mock_terminal_pinset.hpp>

class PinMockFactory {
public:
    template <typename T>
    std::unique_ptr<T> createPin() {
        return std::make_unique<T>();
    }

    template <typename T, typename U>
    std::vector<std::unique_ptr<T>> createGenericPinVec(const int& size) {
        std::vector<std::unique_ptr<T>> vec;
        for (int i = 0; i < size; i++) {
            vec.emplace_back(createPin<U>());
        }
        return vec;
    }

    template <typename T, typename U>
    std::vector<T*> getMockPtrs(std::vector<std::unique_ptr<U>>& genericPinVec) {
        std::vector<T*> pinPtrs;
        for (auto& pin : genericPinVec) {
            pinPtrs.push_back(dynamic_cast<T*>(pin.get()));
        }
        return pinPtrs;
    }
};
