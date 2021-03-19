#pragma once

#include <autogarden/duration_parser.hpp>
#include <autogarden/interfaces/config_parser.hpp>
#include <memory>
#include <vector>

struct WateringStationConfigs {
    uint32_t duration;
    float threshold;
    bool status;
};

class WateringStationConfigParser : public IWateringStationConfigParser<WateringStationConfigs> {
public:
    WateringStationConfigParser(std::unique_ptr<IDurationParser>&& parser) : __pParser(std::move(parser)) {}

    WateringStationConfigs parse(const JsonObject& configs) override {
        __pParser->parse(configs["watering_duration"]);
        auto duration  = __pParser->getMilliSeconds();
        auto threshold = configs["moisture_threshold"];
        auto status    = configs["status"];
        return { duration, threshold, status };
    }

private:
    std::unique_ptr<IDurationParser> __pParser;
};