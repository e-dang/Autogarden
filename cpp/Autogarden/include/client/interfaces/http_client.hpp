#pragma once

#include <Arduino.h>
#include <ArduinoJson.h>

struct HttpRequest {
    String url;
    String method;
    String contentType;
    String authorization;
    DynamicJsonDocument data;

    HttpRequest() : url(), method(), contentType(), data(0) {}

    String toString() const {
        String strData;
        serializeJson(data, strData);
        return strData;
    }
};

struct HttpResponse {
    int statusCode;
    bool processingError;
    String data;
    size_t size = 1024;

    DynamicJsonDocument getJsonData() {
        DynamicJsonDocument json(size);
        deserializeJson(json, data);
        json.shrinkToFit();
        return json;
    }
};

class IHttpClient {
public:
    virtual ~IHttpClient() = default;

    virtual HttpResponse get(const HttpRequest& request) = 0;

    virtual HttpResponse post(const HttpRequest& request) = 0;

    virtual HttpResponse patch(const HttpRequest& request) = 0;

    virtual int getConnectionStrength() const = 0;
};

class IHttpClientFactory {
public:
    virtual ~IHttpClientFactory() = default;

    virtual std::unique_ptr<IHttpClient> create(const String& ssid, const String& password, const int& waitTime) = 0;
};