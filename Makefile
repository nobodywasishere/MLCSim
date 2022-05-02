install:
	python3 -m pip install .

docs:
	mkdir -p docs/docs
	cp docs/*.svg docs/docs
	cp docs/*.png docs/docs
	lazydocs \
		--output-path="./docs/docstrings" \
		--overview-file="REAMDE.md" \
		--ignored-modules simulation,steps,steps_plot \
		--src-base-url "https://github.com/nobodywasishere/MLCSim/blob/master/" \
		mlcsim
	mkdocs build

serve:
	python -m http.server --directory site

format:
	black mlcsim/*.py
	docstr-coverage \
		--skip-init \
		--skip-private \
		--skip-class-def \
		-b docs/badge.svg \
		mlcsim/
	mypy mlcsim

compile: format
	mypyc mlcsim/*.py

clean:
	rm -rf docs/docstrings build site __pycache__ mlcsim/__pycache__ .mypy_cache mlcsim/*.so *.so

.PHONY: install docs format clean