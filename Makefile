HEADLESS := $(if $(CI), --headless, )

install:
	python3 -m pip install -U pip && \
	pip3 install -r requirements.txt

test-u:
	pytest -m unit

test-i:
	pytest -m integration

test-f:
	pytest $(HEADLESS) -m functional

test:
	pytest -m unit && \
	pytest -m integration && \
	pytest -m functional