#pragma once

#include <ESP8266HTTPClient.h>

#include <client/esp8266/wifi_connection.hpp>
#include <client/interfaces/http_client.hpp>

class ESP8266HttpClient : public IHttpClient {
public:
    ESP8266HttpClient(IWifiConnection* connection) : __mClient(), __pConnection(std::move(connection)) {}

    HttpResponse get(const HttpRequest& request) override {
        HttpResponse response;
        if (request.method != "get") {
            response.processingError = true;
            return response;
        }

        __connect();

        __preprocess(request);
        response.statusCode = __mClient.GET();
        __postprocess(response);

        return response;
    }

    HttpResponse post(const HttpRequest& request) override {
        HttpResponse response;
        if (request.method != "post") {
            response.processingError = true;
            return response;
        }

        __connect();

        __preprocess(request);
        response.statusCode = __mClient.POST(request.toString());
        __postprocess(response);

        return response;
    }

private:
    void __connect() {
        if (!__pConnection->isConnected())
            __pConnection->connect();
    }

    void __preprocess(const HttpRequest& request) {
        __mClient.begin(request.url);
        __mClient.addHeader("Content-Type", request.contentType);
    }

    void __postprocess(HttpResponse& response) {
        response.data            = __mClient.getString();
        response.processingError = false;
        __mClient.end();
    }

private:
    HTTPClient __mClient;
    std::unique_ptr<IWifiConnection> __pConnection;
};

class ESP8266HttpClientFactory : public IHttpClientFactory {
public:
    std::unique_ptr<IHttpClient> create(const String& ssid, const String& password,
                                        const int& waitTime = 1000) override {
        auto connection = new WifiConnection(ssid, password, waitTime);
        return std::make_unique<ESP8266HttpClient>(connection);
    }
};