PYTHON_VERSIONS := 3.7 3.8 3.9 3.11 3.12

push:
	. .venv/bin/activate && \
	python setup.py sdist && \
	twine upload dist/* && \
	deactivate
	sudo rm -rf build
	sudo rm -rf *.egg-info

pytest:
	. .venv/bin/activate && \
	$(foreach ver,$(PYTHON_VERSIONS),\
		tox -e py$(ver) &&) \
	deactivate

runtime:
	apt update
	$(foreach ver,$(PYTHON_VERSIONS),\
		$(if $(shell dpkg -l python$(ver) python$(ver)-venv 2>/dev/null | grep -q '^ii'), \
			@echo "Python$(ver) and python$(ver)-venv are already installed",\
			apt install -y python$(ver) python$(ver)-venv;))
