.PHONY: test deploy fix-lint install-develop

test:
	pytest

deploy:
	chalice deploy

fix-lint:
	black *.py chalicelib/*.py
	isort *.py chalicelib/*.py

install-develop:
	pip install -r requirements.txt
	pip install black pytest isort
