#pragma once

#include <Arduino.h>

#include <autogarden/interfaces/duration_parser.hpp>
#include <vector>

class DurationParser : public IDurationParser {
public:
    void parse(const char* duration) override {
        std::vector<int> durations;
        char chars[100];

        strcpy(chars, duration);
        auto ptr = strtok(chars, ":");
        while (ptr != nullptr) {
            durations.push_back(atoi(ptr));
            ptr = strtok(nullptr, ":");
        }

        auto size  = durations.size();
        __mSeconds = durations[size - 1];
        __mMinutes = durations[size - 2];
    }

    uint32_t getMilliSeconds() const override {
        return (__mMinutes * 60 + __mSeconds) * 1000;
    }

private:
    int __mMinutes;
    int __mSeconds;
};