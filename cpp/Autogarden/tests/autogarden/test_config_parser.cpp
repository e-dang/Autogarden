#include <gtest/gtest.h>

#include <autogarden/config_parser.hpp>
#include <mocks/mock_duration_parser.hpp>

using namespace ::testing;

class WateringStationConfigParserTest : public Test {
protected:
    const uint32_t duration = 60000;
    const float threshold   = 50.;
    const bool status       = true;
    DynamicJsonDocument doc;
    NiceMock<MockDurationParser>* mockDurationParser;
    std::unique_ptr<NiceMock<MockDurationParser>> tmpMockDurationParser;
    std::unique_ptr<WateringStationConfigParser> parser;

    WateringStationConfigParserTest() : doc(1024), tmpMockDurationParser(new NiceMock<MockDurationParser>()) {
        mockDurationParser        = tmpMockDurationParser.get();
        parser                    = std::make_unique<WateringStationConfigParser>(std::move(tmpMockDurationParser));
        doc["watering_duration"]  = duration;
        doc["moisture_threshold"] = threshold;
        doc["status"]             = status;
    }
};

TEST_F(WateringStationConfigParserTest, parse_returns_configs_with_duration_correctly_parsed) {
    EXPECT_CALL(*mockDurationParser, getMilliSeconds()).WillOnce(Return(duration));

    auto configs = parser->parse(doc.as<JsonObject>());

    EXPECT_EQ(configs.duration, duration);
}

TEST_F(WateringStationConfigParserTest, parse_returns_configs_with_threshold_correctly_parsed) {
    auto configs = parser->parse(doc.as<JsonObject>());

    EXPECT_FLOAT_EQ(configs.threshold, threshold);
}

TEST_F(WateringStationConfigParserTest, parse_returns_configs_with_status_correctly_parsed) {
    auto configs = parser->parse(doc.as<JsonObject>());

    EXPECT_EQ(configs.status, status);
}
