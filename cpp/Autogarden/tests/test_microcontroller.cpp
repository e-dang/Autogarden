#include <gmock/gmock.h>
#include <gtest/gtest.h>

#include <components/microcontroller.hpp>
#include <memory>
#include <numeric>

#include "mock_terminal_pin_set.hpp"

using namespace ::testing;

class MicroControllerTest : public Test
{
protected:
    std::string id = "controller";
    MockTerminalPinSet<DigitalPin> digitalPins;
    MockTerminalPinSet<AnalogOutputPin> analogOutputPins;
    MockTerminalPinSet<AnalogInputPin> analogInputPins;
    std::unique_ptr<MicroController> controller;

    MicroControllerTest() : digitalPins(), analogOutputPins(), analogInputPins()
    {
        controller = std::make_unique<MicroController>(id, &digitalPins, &analogOutputPins, &analogInputPins);
    }
};

template <typename T>
void assertGetPinNumsIsCorrect(std::function<std::vector<uint8_t>(void)>& getPins, T& mockPins)
{
    std::vector<uint8_t> retVec = { 0, 1, 2 };
    ON_CALL(mockPins, getPinNumbers()).WillByDefault(Return(retVec));
    EXPECT_CALL(mockPins, getPinNumbers());

    auto retVal = getPins();

    ASSERT_THAT(retVal, ContainerEq(retVec));
}

TEST_F(MicroControllerTest, getDigitalPinNums)
{
    std::function<std::vector<uint8_t>(void)> func = [this]() { return this->controller->getDigitalPinNums(); };

    assertGetPinNumsIsCorrect(func, digitalPins);
}

TEST_F(MicroControllerTest, getAnalogOutputPinNums)
{
    std::function<std::vector<uint8_t>(void)> func = [this]() { return this->controller->getAnalogOutputPinNums(); };

    assertGetPinNumsIsCorrect(func, analogOutputPins);
}

TEST_F(MicroControllerTest, getAnalogInputPinNums)
{
    std::function<std::vector<uint8_t>(void)> func = [this]() { return this->controller->getAnalogInputPinNums(); };

    assertGetPinNumsIsCorrect(func, analogInputPins);
}

template <typename T>
void assertGetNumAvailableOutputPinsWorks(const int& numRequested, const PinMode& pinMode,
                                          std::function<std::vector<PinView>(const int&, const PinMode&)>& func,
                                          T& mockPins)
{
    std::vector<PinView> retVec(numRequested, nullptr);
    ON_CALL(mockPins, getNextAvailable(numRequested)).WillByDefault(Return(retVec));
    EXPECT_CALL(mockPins, getNextAvailable(numRequested));

    auto retVal = func(numRequested, pinMode);

    ASSERT_EQ(retVec.size(), retVal.size());
}

TEST_F(MicroControllerTest, getNumAvailableOutputPinsWhenModeIsDigital)
{
    std::function<std::vector<PinView>(const int&, const PinMode&)> func = [this](const int& numAvailable,
                                                                                  const PinMode& pinMode) {
        return this->controller->getNumAvailableOutputPins(numAvailable, pinMode);
    };

    assertGetNumAvailableOutputPinsWorks(3, PinMode::Digital, func, digitalPins);
}

TEST_F(MicroControllerTest, getNumAvailableOutputPinsWhenModeIsAnalogOutput)
{
    std::function<std::vector<PinView>(const int&, const PinMode&)> func = [this](const int& numAvailable,
                                                                                  const PinMode& pinMode) {
        return this->controller->getNumAvailableOutputPins(numAvailable, pinMode);
    };

    assertGetNumAvailableOutputPinsWorks(3, PinMode::AnalogOutput, func, analogOutputPins);
}

TEST_F(MicroControllerTest, getNumAvailableOutputPinsWhenModeIsAnalogInput)
{
    std::function<std::vector<PinView>(const int&, const PinMode&)> func = [this](const int& numAvailable,
                                                                                  const PinMode& pinMode) {
        return this->controller->getNumAvailableOutputPins(numAvailable, pinMode);
    };

    assertGetNumAvailableOutputPinsWorks(3, PinMode::AnalogInput, func, analogInputPins);
}

TEST_F(MicroControllerTest, getId) { EXPECT_EQ(controller->getId(), id); }

TEST_F(MicroControllerTest, parentIsNull) { EXPECT_EQ(controller->getParent(), nullptr); }

TEST_F(MicroControllerTest, hasParentReturnsWhenParentIsNull) { EXPECT_FALSE(controller->hasParent()); }

template <typename T>
bool setUpHasNumAvailableOutputPinsTest(const int& numAvailable, const int& requestedNum, const PinMode& pinMode,
                                        std::function<bool(const int&, const PinMode&)>& func, T& mockPins)
{
    ON_CALL(mockPins, getNumAvailable()).WillByDefault(Return(numAvailable));
    EXPECT_CALL(mockPins, getNumAvailable());
    return func(requestedNum, pinMode);
}

TEST_F(MicroControllerTest, hasNumAvailableOutputPinsReturnsFalseWhenRequestedNumDigitalPinsIsLargerThanAvailablePins)
{
    const auto numAvailable                              = 10;
    const auto requestedNum                              = numAvailable + 1;
    const auto pinMode                                   = PinMode::Digital;
    std::function<bool(const int&, const PinMode&)> func = [this](const int& numRequested, const PinMode& pinMode) {
        return this->controller->hasNumAvailableOutputPins(numRequested, pinMode);
    };

    EXPECT_FALSE(setUpHasNumAvailableOutputPinsTest(numAvailable, requestedNum, pinMode, func, digitalPins));
}

TEST_F(MicroControllerTest,
       hasNumAvailableOutputPinsReturnsFalseWhenRequestedNumAnalogOutputPinsIsLargerThanAvailablePins)
{
    const auto numAvailable                              = 10;
    const auto requestedNum                              = numAvailable + 1;
    const auto pinMode                                   = PinMode::AnalogOutput;
    std::function<bool(const int&, const PinMode&)> func = [this](const int& numRequested, const PinMode& pinMode) {
        return this->controller->hasNumAvailableOutputPins(numRequested, pinMode);
    };

    EXPECT_FALSE(setUpHasNumAvailableOutputPinsTest(numAvailable, requestedNum, pinMode, func, analogOutputPins));
}

TEST_F(MicroControllerTest,
       hasNumAvailableOutputPinsReturnsFalseWhenRequestedNumAnalogInputPinsIsLargerThanAvailablePins)
{
    const auto numAvailable                              = 10;
    const auto requestedNum                              = numAvailable + 1;
    const auto pinMode                                   = PinMode::AnalogInput;
    std::function<bool(const int&, const PinMode&)> func = [this](const int& numRequested, const PinMode& pinMode) {
        return this->controller->hasNumAvailableOutputPins(numRequested, pinMode);
    };

    EXPECT_FALSE(setUpHasNumAvailableOutputPinsTest(numAvailable, requestedNum, pinMode, func, analogInputPins));
}