#include <Arduino.h>

void setMockArduino(ArduinoInterface* mockArduino) {
    ::arduino = mockArduino;
}

void digitalWrite(const uint8_t& pin, const int& value) {
    if (::arduino != nullptr) {
        ::arduino->_digitalWrite(pin, value);
    }
}

int digitalRead(const uint8_t& pin) {
    if (::arduino != nullptr) {
        return ::arduino->_digitalRead(pin);
    }
    return 0;
}

void analogWrite(const uint8_t& pin, const int& value) {
    if (::arduino != nullptr) {
        ::arduino->_analogWrite(pin, value);
    }
}

int analogRead(const uint8_t& pin) {
    if (::arduino != nullptr) {
        return ::arduino->_analogRead(pin);
    }
    return 0;
}

void shiftOut(const uint8_t& dataPin, const uint8_t& clockPin, const int& direction, const int& data) {
    if (::arduino != nullptr) {
        ::arduino->_shiftOut(dataPin, clockPin, direction, data);
    }
}

void pinMode(const uint8_t& pin, const int& direction) {
    if (::arduino != nullptr) {
        ::arduino->_pinMode(pin, direction);
    }
}

void delay(const uint32_t& time) {
    if (::arduino != nullptr) {
        ::arduino->_delay(time);
    }
}