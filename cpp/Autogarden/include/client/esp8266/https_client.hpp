#pragma once

#include <CertStoreBearSSL.h>
#include <ESP8266HTTPClient.h>
#include <FS.h>
#include <LittleFS.h>
#include <time.h>

#include <client/esp8266/http_client.hpp>

class BearSSLWrapper {
public:
    void initialize() {
        setClock();
        loadCerts();
    }

    WiFiClient& getWifiClient() {
        return dynamic_cast<WiFiClient&>(__mClient);
    }

    void loadCerts() {
        LittleFS.begin();
        int numCerts = __mCertStore.initCertStore(LittleFS, PSTR("/certs.idx"), PSTR("/certs.ar"));
        __mClient.setCertStore(&__mCertStore);
    }

    void setClock() {
        configTime(3 * 3600, 0, "pool.ntp.org", "time.nist.gov");

        Serial.print("Waiting for NTP time sync: ");
        time_t now = time(nullptr);
        while (now < 8 * 3600 * 2) {
            delay(500);
            Serial.print(".");
            now = time(nullptr);
        }
        Serial.println("");
        struct tm timeinfo;
        gmtime_r(&now, &timeinfo);
        Serial.print("Current time: ");
        Serial.print(asctime(&timeinfo));
    }

private:
    BearSSL::WiFiClientSecure __mClient;
    BearSSL::CertStore __mCertStore;
};

class ESP8266HttpsClient : public ESP8266HttpClient {
public:
    ESP8266HttpsClient(std::unique_ptr<IWifiConnection>&& connection, std::unique_ptr<BearSSLWrapper>&& wrapper) :
        ESP8266HttpClient(std::move(connection)), __pBearSSL(std::move(wrapper)) {}

protected:
    void _preprocess(const HttpRequest& request) override {
        _mClient.begin(__pBearSSL->getWifiClient(), request.url);
        _mClient.addHeader("Content-Type", request.contentType);
        _mClient.addHeader("Authorization", "Token " + request.authorization);
    }

private:
    std::unique_ptr<BearSSLWrapper> __pBearSSL;
};

class ESP8266HttpsClientFactory : public IHttpClientFactory {
public:
    std::unique_ptr<IHttpClient> create(const String& ssid, const String& password,
                                        const int& waitTime = 1000) override {
        std::unique_ptr<BearSSLWrapper> wrapper = std::make_unique<BearSSLWrapper>();
        wrapper->initialize();
        std::unique_ptr<IWifiConnection> connection = std::make_unique<WifiConnection>(ssid, password, waitTime);
        return std::make_unique<ESP8266HttpsClient>(std::move(connection), std::move(wrapper));
    }
};