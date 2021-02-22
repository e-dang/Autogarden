#pragma once
#include <Arduino.h>
#include <gmock/gmock.h>

class MockArduino : public ArduinoInterface {
public:
    MOCK_METHOD(void, _digitalWrite, (const uint8_t& pin, const int& value), (const, override));
    MOCK_METHOD(int, _digitalRead, (const uint8_t& pin), (const, override));
    MOCK_METHOD(void, _analogWrite, (const uint8_t& pin, const int& value), (const, override));
    MOCK_METHOD(int, _analogRead, (const uint8_t& pin), (const, override));
    MOCK_METHOD(void, _shiftOut,
                (const uint8_t& dataPin, const uint8_t& clockPin, const int& direction, const int& data),
                (const, override));
    MOCK_METHOD(void, _pinMode, (const uint8_t& pin, const int& direction), (const, override));
    MOCK_METHOD(void, _delay, (const uint32_t& time), (const, override));
};