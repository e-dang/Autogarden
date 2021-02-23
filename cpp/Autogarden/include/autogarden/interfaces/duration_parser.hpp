#pragma once

class IDurationParser {
public:
    virtual ~IDurationParser() = default;

    virtual void parse(const char* duration) = 0;

    virtual uint32_t getMilliSeconds() const = 0;
};