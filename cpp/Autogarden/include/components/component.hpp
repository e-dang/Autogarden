#pragma once

#include <Arduino.h>

#include <pins/pins.hpp>

class Component;

class IComponent {
public:
    virtual ~IComponent() = default;

    virtual bool appendChild(std::shared_ptr<Component> component) = 0;

    virtual Component* getChild(const String& id) = 0;

    virtual int getNumChildren() const = 0;

    virtual const Component* getParent() const = 0;

    virtual String getId() const = 0;

    virtual Component* getRoot() = 0;

    virtual bool hasParent() const = 0;

    virtual bool isRoot() const = 0;
};

class Component : public IComponent {
public:
    Component(const String& id) : __mId(id), _pRoot(nullptr), _pParent(nullptr), __mChildren(0) {}

    virtual ~Component() = default;

    bool appendChild(std::shared_ptr<Component> component) override {
        if (component != nullptr && component->_setInputPins(this)) {
            __mChildren.push_back(component);
            component->_pParent = this;
            component->_pRoot   = _pRoot;
            return true;
        }

        return false;
    }

    Component* getChild(const String& id) override {
        if (getId() == id)
            return this;

        for (auto& child : __mChildren) {
            auto target = child->getChild(id);
            if (target != nullptr)
                return target;
        }

        return nullptr;
    }

    int getNumChildren() const override {
        return static_cast<int>(__mChildren.size());
    }

    const Component* getParent() const override {
        return _pParent;
    };

    Component* getRoot() override {
        return _pRoot;
    }

    String getId() const override {
        return __mId;
    }

    bool hasParent() const override {
        return getParent() != nullptr;
    }

    bool isRoot() const override {
        return _pRoot == this;
    }

protected:
    virtual bool _setInputPins(Component* parent) = 0;

    virtual IOutputPinSet* _getOutputPins() = 0;

    IOutputPinSet* _getComponentOutputPins(Component* component) {
        if (component == nullptr)
            return nullptr;

        return component->_getOutputPins();
    }

    virtual bool _propagateSignal() {
        if (_pParent != nullptr)
            return _pParent->_propagateSignal();

        return false;
    }

protected:
    Component* _pRoot;
    Component* _pParent;
    std::vector<std::shared_ptr<Component>> __mChildren;

private:
    String __mId;
};
