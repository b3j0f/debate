PLATFORM := dev
BIND := 127.0.0.1:8000
SETTINGS := DJANGO_SETTINGS_MODULE="app.settings.$(PLATFORM)"
DJANGO := $(SETTINGS) python manage.py
LOADDATA := $(DJANGO) loaddata
PYTHON := python2.7

.PHONY: all
all: migrations migrate fixtures

.PHONY: migrations
migrations:
	$(DJANGO) makemigrations core

.PHONY: migrate
migrate: migrations
	$(DJANGO) migrate

.PHONY: fixtures
fixtures:
	$(LOADDATA) forbiddendomains eventtypes

.PHONY: superuser
superuser:
	$(LOADDATA) users

.PHONY: static
static:
	$(DJANGO) collectstatic

.PHONY: run
run: static
	$(DJANGO) runserver $(BIND)

.PHONY: runshell
shell:
	$(DJANGO) shell

.PHONY: install_deps
install_deps:
	pip install -r requirements/$(PLATFORM).txt

.PHONY: venv
venv:
	virtualenv venv -p $(PYTHON)
	source venv/bin/activate

.PHONY: graph_models # require dev environment
graph_models:
	$(DJANGO) graph_models -a > graph_models.dot
	$(DJANGO) graph_models -a -g -o graph_models.png

.PHONY: clean
clean:
	rm -rf www/*

.PHONY: clean-hard
clean-hard: clean
	rm -rf */migrations/0* ; $(DJANGO) dumpdata > dumped ; $(DJANGO) flush ; rm -rf db.sqlite3 ; rm -rf venv
