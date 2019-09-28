.PHONY: clean-pyc

help:
	@echo "    init"
	@echo "        Initializes project requirements"
	@echo "    clean-pyc"
	@echo "        Remove python artifacts."
	@echo "    lint"
	@echo "        Run lint script on application."
	@echo "    test"
	@echo "        Run pytest locally"
	@echo "    start"
	@echo "        Runs application in dev mode."

clean-pyc:
	@find . -name '*.pyc' -exec rm -f {} +
	@find . -name '*.pyo' -exec rm -f {} +
	@find . -name '*~' -exec rm -f {} +
	@find . -name '__pycache__' -exec rm -fr {} +

lint:
	@./scripts/lint

test:
	@./scripts/test

start:
	@./scripts/start
