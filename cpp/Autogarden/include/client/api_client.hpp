#pragma once

#include <Arduino.h>
#include <ArduinoJson.h>

#include <client/esp8266/http_client.hpp>
#include <client/interfaces/api_client.hpp>
#include <client/interfaces/http_client.hpp>

class APIClient : public IAPIClient {
public:
    APIClient(const String& gardenName, const String& apiKey, const String& rootUrl,
              std::unique_ptr<IHttpClient>&& client, const String& contentType = "application/json") :
        __mGardenName(gardenName),
        __mAPIKey(apiKey),
        __mRootUrl(rootUrl),
        __mContentType(contentType),
        __pClient(std::move(client)) {
        __mGardenName.replace(" ", "%20");
    }

    DynamicJsonDocument getWateringStationConfigs() const override {
        HttpRequest request;
        request.url           = _getWateringStationsUrl();
        request.method        = "get";
        request.contentType   = __mContentType;
        request.authorization = __mAPIKey;

        HttpResponse response;
        while (true) {
            response = __pClient->get(request);
            if (response.statusCode > 0)
                break;
        }

        return response.getJsonData();
    }

    DynamicJsonDocument getGardenConfigs() const override {
        HttpRequest request;
        request.url           = _getGardenUrl();
        request.method        = "get";
        request.contentType   = __mContentType;
        request.authorization = __mAPIKey;

        HttpResponse response;
        while (true) {
            response = __pClient->get(request);
            if (response.statusCode > 0)
                break;
        }

        return response.getJsonData();
    }

    void sendGardenData(const DynamicJsonDocument& data) const override {
        HttpRequest request;
        request.url           = _getGardenUrl();
        request.method        = "patch";
        request.contentType   = __mContentType;
        request.authorization = __mAPIKey;
        request.data          = data;

        HttpResponse response;
        while (true) {
            response = __pClient->patch(request);
            if (response.statusCode > 0)
                break;
        }
    }

    void sendWateringStationData(const DynamicJsonDocument& data) const override {
        HttpRequest request;
        request.url           = _getWateringStationsUrl();
        request.method        = "post";
        request.contentType   = __mContentType;
        request.authorization = __mAPIKey;
        request.data          = data;

        HttpResponse response;
        while (true) {
            response = __pClient->post(request);
            if (response.statusCode > 0)
                break;
        }
    }

    int getConnectionStrength() const override {
        return __pClient->getConnectionStrength();
    }

protected:
    String _getWateringStationsUrl() const {
        return _getGardenUrl() + "watering-stations/";
    }

    String _getGardenUrl() const {
        auto url = __mRootUrl + "api/gardens/<?>/";
        url.replace("<?>", __mGardenName);
        return url;
    }

private:
    String __mGardenName;
    String __mRootUrl;
    String __mContentType;
    String __mAPIKey;
    std::unique_ptr<IHttpClient> __pClient;
};

class APIClientFactory : public IAPIClientFactory {
public:
    APIClientFactory(std::unique_ptr<IHttpClientFactory>&& httpClientFactory) :
        __pHttpClientFactory(std::move(httpClientFactory)) {}

    std::unique_ptr<IAPIClient> create(const String& gardenName, const String& apiKey, const String& ssid,
                                       const String& password, const String& rootUrl,
                                       const int& waitTime = 1000) override {
        auto httpClient = __pHttpClientFactory->create(ssid, password, waitTime);
        return std::make_unique<APIClient>(gardenName, apiKey, rootUrl, std::move(httpClient));
    }

private:
    std::unique_ptr<IHttpClientFactory> __pHttpClientFactory;
};