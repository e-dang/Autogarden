#pragma once

#include <pins/pins.hpp>
#include <string>

class Component
{
public:
    Component(const std::string& id) : __mId(id), _pParent(nullptr), _mChildren(0) {}

    virtual ~Component() = default;

    bool appendChild(Component* component)
    {
        if (component != nullptr && component->_setInputPins(this))
        {
            _mChildren.push_back(component);
            component->_setParent(this);
            return true;
        }
        return false;
    }

    Component* getChild(const std::string& id)
    {
        if (__mId == id)
            return this;

        for (int i = 0; i < getNumChildren(); i++)
        {
            auto component = _mChildren[i]->getChild(id);
            if (component != nullptr)
                return component;
        }

        return nullptr;
    }

    std::string getId() const { return __mId; }

    Component* getParent() { return _pParent; }

    int getNumChildren() const { return static_cast<int>(_mChildren.size()); }

    bool hasParent() { return getParent() != nullptr; }

    virtual void run() = 0;

    virtual bool hasNumAvailableOutputPins(const int& requestedNum, const PinMode& pinMode) = 0;

    virtual std::vector<PinView> getNumAvailableOutputPins(const int& requestedNum, const PinMode& pinMode) = 0;

protected:
    virtual bool _setInputPins(Component* parent) = 0;

    bool _setParent(Component* component)
    {
        if (component != nullptr)
        {
            _pParent = component;
            return true;
        }
        return false;
    }

protected:
    Component* _pParent;
    std::vector<Component*> _mChildren;

private:
    std::string __mId;
};
