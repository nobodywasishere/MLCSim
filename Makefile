install:
	python3 -m pip install .

docs:
	lazydocs \
		--output-path="./docs/docstrings" \
		--overview-file="REAMDE.md" \
		--ignored-modules simulation,steps,steps_plot \
		--src-base-url "https://github.com/nobodywasishere/MLCSim/blob/master/" \
		MLCSim
	mkdocs build

serve:
	python -m http.server --directory site

format:
	black MLCSim/*.py
	docstr-coverage \
		--skip-init \
		--skip-private \
		--skip-class-def \
		-b docs/badge.svg \
		MLCSim/

.PHONY: install docs format