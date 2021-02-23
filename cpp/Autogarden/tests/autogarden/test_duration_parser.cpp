#include <gmock/gmock.h>
#include <gtest/gtest.h>

#include <autogarden/duration_parser.hpp>

TEST(DurationParserTest, parse_get_correct_number_of_milliseconds) {
    DurationParser parser;
    parser.parse("00:01:01");
    auto minutes      = 1;
    auto seconds      = 1;
    auto milliseconds = (minutes * 60 + seconds) * 1000;

    EXPECT_EQ(parser.getMilliSeconds(), milliseconds);
}