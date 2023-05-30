.DEFAULT_GOAL := install

.venv:
	python3.11 -m venv .venv

.PHONY: install
install: .venv
	pip install -r requirements.txt
