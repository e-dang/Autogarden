PROJECT_DIR := `dirname $(abspath $(MAKEFILE_LIST))`
HEADLESS := $(if $(CI), --headless, )
CPP_DIR := $(PROJECT_DIR)/cpp/Autogarden

install:
	python3 -m pip install -U pip && \
	pip3 install -r requirements.txt

test-u:
	pytest -m unit

test-i:
	pytest -m integration

test-f:
	pytest $(HEADLESS) -m functional

test-cpp:
	cd $(CPP_DIR) && \
	if [ -d "build" ]; then \
		cd build && \
		make && \
		./test_autogarden; \
	fi

test:
	pytest -m unit && \
	pytest -m integration && \
	pytest -m functional