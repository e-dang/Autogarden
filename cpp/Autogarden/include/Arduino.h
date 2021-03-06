#pragma once

#include <stdint.h>

#include <string>

class String : public std::string {
public:
    String() : std::string() {}

    String(int i) : std::string(std::to_string(i)) {}

    String(const char* str) : std::string(str) {}

    String(std::string& str) : std::string(str) {}
};

class ArduinoInterface {
public:
    virtual ~ArduinoInterface() = default;

    virtual void _digitalWrite(const uint8_t& pin, const int& value) const = 0;

    virtual int _digitalRead(const uint8_t& pin) const = 0;

    virtual void _analogWrite(const uint8_t& pin, const int& value) const = 0;

    virtual int _analogRead(const uint8_t& pin) const = 0;

    virtual void _shiftOut(const uint8_t& dataPin, const uint8_t& clockPin, const int& direction,
                           const int& data) const = 0;

    virtual void _pinMode(const uint8_t& pin, const int& direction) const = 0;

    virtual void _delay(const uint32_t& time) const = 0;
};

class Arduino : public ArduinoInterface {
public:
    virtual ~Arduino() = default;

    void _digitalWrite(const uint8_t& pin, const int& value) const override {}

    int _digitalRead(const uint8_t& pin) const override {
        return 0;
    }

    void _analogWrite(const uint8_t& pin, const int& value) const override {}

    int _analogRead(const uint8_t& pin) const override {
        return 0;
    }

    void _shiftOut(const uint8_t& dataPin, const uint8_t& clockPin, const int& direction,
                   const int& data) const override {}

    void _pinMode(const uint8_t& pin, const int& direction) const override {}

    void _delay(const uint32_t& time) const override {}
};

namespace
{
ArduinoInterface* arduino = nullptr;
}

void setMockArduino(ArduinoInterface* mockArduino);

void digitalWrite(const uint8_t& pin, const int& value);

int digitalRead(const uint8_t& pin);

void analogWrite(const uint8_t& pin, const int& value);

int analogRead(const uint8_t& pin);

void shiftOut(const uint8_t& dataPin, const uint8_t& clockPin, const int& direction, const int& data);

void pinMode(const uint8_t& pin, const int& direction);

void delay(const uint32_t& time);
