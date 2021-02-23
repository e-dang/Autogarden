#include <autogarden.h>

AutoGardenConfigs configs = {
    "controller",
    { D2, D3, D4, D8, D9, D5, D6 },
    {},
    {},
    { A0 },
    "reg",
    8,
    MSBFIRST,
    "dMux",
    4,
    16,
    PinMode::DigitalOutput,
    "aMux",
    4,
    16,
    PinMode::AnalogInput,
    "pump",
    HIGH,
    LOW,
    "sensor",
    0.,
    "valve",
    HIGH,
    LOW,
    { 16,    // num watering stations
      "" },  // random UUID
    60000,   // milliseconds delay per loop
    "",      // ssid
    "",      // wifi password
    ""       // domain name of server
};

std::unique_ptr<IAutoGarden> autogarden;

std::unique_ptr<IAutoGarden> createAutoGarden() {
    auto componentFactory =
      std::make_unique<ComponentFactory>(std::make_unique<SignalFactory>(), std::make_unique<PinFactory>());
    auto clientFactory = std::make_unique<APIClientFactory>(std::make_unique<ESP8266HttpClientFactory>());
    AutoGardenFactory factory(&configs, std::move(componentFactory), std::move(clientFactory));
    return factory.create();
}

void setup() {
    Serial.begin(9600);
    autogarden = createAutoGarden();
    autogarden->initializePins();
    autogarden->initializeServer();
}

void loop() {
    autogarden->refreshWateringStations();
    autogarden->run();
    delay(configs.millisecondDelay);
}