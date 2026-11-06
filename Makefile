# VENV := .venv
VENV := /usr
PYTHON := $(VENV)/bin/python
PIP := $(VENV)/bin/pip
ENTRY := main.py

.PHONY: help setup install run clean

help:
	@echo "Commandes disponibles :"
	@echo "  make setup    - crée le venv et installe les dépendances"
	@echo "  make install  - installe / met à jour les dépendances"
	@echo "  make run      - lance le jeu"
	@echo "  make clean    - supprime le venv et les caches Python"

$(VENV):
	python3 -m venv $(VENV)

install: $(VENV)
	$(PIP) install --upgrade pip
	$(PIP) install pygame

setup: install
	@echo "Environnement prêt. Lance ton jeu avec : make run"

run:
	$(PYTHON) $(ENTRY)

clean:
	rm -rf .pytest_cache __pycache__ **/__pycache__
