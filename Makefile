# Require a virtual environment to be active
ifndef VIRTUAL_ENV
$(error Virtual environment not active. Run: source venv/bin/activate)
endif

PYTHON := python3

.PHONY: data validate features validate-features all

data:
	$(PYTHON) generate_data.py

validate:
	$(PYTHON) src/validate_data.py

features:
	$(PYTHON) src/generate_features.py

validate-features:
	$(PYTHON) src/validate_features.py

all: data validate features validate-features