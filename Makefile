PROJECT_DIR := `dirname $(abspath $(MAKEFILE_LIST))`
HEADLESS := $(if $(CI), --headless, )
THREADS := $(if $(CI), -j2, -j4)
CPP_DIR := $(PROJECT_DIR)/cpp/Autogarden

install:
	python3 -m pip install -U pip && \
	pip3 install -r requirements.txt && \
	npm install

build:
	npm run prod

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
		make $(THREADS) && \
		./test_autogarden; \
	fi

test:
	pytest -m unit && \
	pytest -m integration && \
	pytest -m functional && \
	make test-cpp

deploy: install build
	python3 manage.py migrate && \
	python3 manage.py collectstatic