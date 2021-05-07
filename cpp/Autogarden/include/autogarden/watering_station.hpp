#pragma once

#include <autogarden/config_parser.hpp>
#include <autogarden/interfaces/watering_station.hpp>
#include <components/components.hpp>

class WateringStation : public IWateringStation {
public:
    WateringStation(const int& idx, const bool& status, const uint32_t& duration, const float& threshold,
                    std::shared_ptr<IPump> pump, std::shared_ptr<IValve> valve, std::shared_ptr<IMoistureSensor> sensor,
                    std::shared_ptr<IWateringStationConfigParser<WateringStationConfigs>> parser) :
        __mIdx(idx),
        __mStatus(status),
        __mDuration(duration),
        __mThreshold(threshold),
        __mCurrData(256),
        __pPump(pump),
        __pValve(valve),
        __pSensor(sensor),
        __pParser(parser) {}

    void activate() override {
        auto reading                  = __pSensor->readScaled();
        __mCurrData["moisture_level"] = reading;
        if (isActive() && reading < __mThreshold) {
            __pValve->open();
            __pPump->start();
            delay(__mDuration);
            __pPump->stop();
            __pValve->close();
        }
    }

    bool update(const JsonObject& configs) override {
        auto parsedConfigs = __pParser->parse(configs);
        if (setThreshold(parsedConfigs.threshold)) {
            setStatus(parsedConfigs.status);
            setDuration(parsedConfigs.duration);
            return true;
        }
        return false;
    }

    void setDuration(const uint32_t& duration) {
        __mDuration = duration;
    }

    bool setThreshold(const float& threshold) {
        if (threshold < 0. || threshold > 100.)
            return false;

        __mThreshold = threshold;
        return true;
    }

    void setStatus(const bool& status) {
        __mStatus = status;
    }

    int getIdx() const override {
        return __mIdx;
    }

    uint32_t getDuration() const {
        return __mDuration;
    }

    int getThreshold() const {
        return __mThreshold;
    }

    bool isActive() const {
        return __mStatus;
    }

    JsonObjectConst getData() const override {
        return __mCurrData.as<JsonObjectConst>();
    }

private:
    int __mIdx;
    bool __mStatus;
    uint32_t __mDuration;
    float __mThreshold;
    DynamicJsonDocument __mCurrData;
    std::shared_ptr<IPump> __pPump;
    std::shared_ptr<IValve> __pValve;
    std::shared_ptr<IMoistureSensor> __pSensor;
    std::shared_ptr<IWateringStationConfigParser<WateringStationConfigs>> __pParser;
};

class SimpleWateringStation : public IWateringStation {
public:
    SimpleWateringStation(const int& idx, const bool& status, const uint32_t& duration, std::shared_ptr<IPump> pump,
                          std::shared_ptr<IWateringStationConfigParser<WateringStationConfigs>> parser) :
        __mIdx(idx), __mStatus(status), __mDuration(duration), __mCurrData(256), __pPump(pump), __pParser(parser) {}

    void activate() override {
        __mCurrData["moisture_level"] = 0.;
        if (isActive()) {
            __pPump->start();
            delay(__mDuration);
            __pPump->stop();
        }
    }

    bool update(const JsonObject& configs) override {
        auto parsedConfigs = __pParser->parse(configs);
        setStatus(parsedConfigs.status);
        setDuration(parsedConfigs.duration);
        return true;
    }

    void setDuration(const uint32_t& duration) {
        __mDuration = duration;
    }

    void setStatus(const bool& status) {
        __mStatus = status;
    }

    int getIdx() const override {
        return __mIdx;
    }

    uint32_t getDuration() const {
        return __mDuration;
    }

    bool isActive() const {
        return __mStatus;
    }

    JsonObjectConst getData() const override {
        return __mCurrData.as<JsonObjectConst>();
    }

private:
    int __mIdx;
    bool __mStatus;
    uint32_t __mDuration;
    DynamicJsonDocument __mCurrData;
    std::shared_ptr<IPump> __pPump;
    std::shared_ptr<IWateringStationConfigParser<WateringStationConfigs>> __pParser;
};
