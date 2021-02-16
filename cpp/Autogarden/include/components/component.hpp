#pragma once

#include <pins/pins.hpp>
#include <string>

class Component {
public:
    Component(const std::string& id) : __mId(id), _pParent(nullptr), __mChildren(0) {}

    virtual ~Component() = default;

    bool appendChild(Component* component) {
        if (component != nullptr && component->_setInputPins(_getOutputPins())) {
            __mChildren.push_back(component);
            component->_pParent = this;
            return true;
        }

        return false;
    }

    Component* getChild(const std::string& id) {
        if (getId() == id)
            return this;

        for (auto& child : __mChildren) {
            auto target = child->getChild(id);
            if (target != nullptr)
                return target;
        }

        return nullptr;
    }

    int getNumChildren() const {
        return static_cast<int>(__mChildren.size());
    }

    const Component* getParent() const {
        return _pParent;
    };

    std::string getId() const {
        return __mId;
    }

    bool hasParent() const {
        return getParent() != nullptr;
    }

protected:
    virtual IOutputPinSet* _getOutputPins() = 0;

    virtual bool _setInputPins(IOutputPinSet* parentOutputPins) = 0;

    virtual bool _propagateSignal() {
        if (_pParent != nullptr)
            return _pParent->_propagateSignal();

        return false;
    }

protected:
    Component* _pParent;
    std::vector<Component*> __mChildren;

private:
    std::string __mId;
};
