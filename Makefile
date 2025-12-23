# Require a virtual environment to be active
ifndef VIRTUAL_ENV
$(error Virtual environment not active. Run: source venv/bin/activate)
endif

PYTHON := python3

.PHONY: data validate all

data:
	$(PYTHON) generate_data.py

validate:
	$(PYTHON) src/validate_data.py

all: data validate
