install:
	python3 -m pip install .

docs:
	lazydocs \
		--output-path="./docs/docstrings" \
		--overview-file="REAMDE.md" \
		MLCSim
	mkdocs build
	python -m http.server --directory site

format:
	black MLCSim/*.py

.PHONY: install docs format