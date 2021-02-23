#pragma once

#include <gmock/gmock.h>

#include <autogarden/interfaces/duration_parser.hpp>

class MockDurationParser : public IDurationParser {
public:
    MOCK_METHOD(void, parse, (const char* duration), (override));
    MOCK_METHOD(uint32_t, getMilliSeconds, (), (const, override));
};