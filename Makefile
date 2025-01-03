.PHONY: clean build install setup_env requirements init_env core_demo client_demo all
clean:
	@rm -rf dist

build:
	@python3 -m build

install:
	@python3 -m pip install -e .

setup_env:
	@python3 -m venv env

requirements:
	@env/bin/python3 -m pip install -r requirements.txt

init_env: setup_env requirements

core_demo:
	@cd tests && python3 core_demo.py

client_demo:
	@cd tests && python3 client_demo.py

all: clean build install
