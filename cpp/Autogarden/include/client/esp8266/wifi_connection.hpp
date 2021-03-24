#pragma once

#include <Arduino.h>
#include <ESP8266WiFi.h>

#include <client/esp8266/interfaces/wifi_connection.hpp>

class WifiConnection : public IWifiConnection {
public:
    WifiConnection(const String& ssid, const String& password, const int& waitTime = 1000) :
        __mSSID(ssid), __mPassword(password), __mWaitTime(waitTime) {}

    void connect() override {
        WiFi.begin(__mSSID, __mPassword);
        while (!isConnected()) {
            delay(__mWaitTime);
        }
    }

    bool isConnected() override {
        return WiFi.status() == WL_CONNECTED;
    }

    int getConnectionStrength() const override {
        return WiFi.RSSI();
    }

private:
    String __mSSID;
    String __mPassword;
    int __mWaitTime;
};