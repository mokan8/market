# Require a virtual environment to be active
ifndef VIRTUAL_ENV
$(error Virtual environment not active. Run: source venv/bin/activate)
endif

PYTHON := python3

.PHONY: data validate features all

data:
	$(PYTHON) generate_data.py

validate:
	$(PYTHON) src/validate_data.py

features:
	$(PYTHON) src/generate_features.py

all: data validate features