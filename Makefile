install:
	@poetry install
	@poetry run pre-commit install

pre-commit-check:
	@poetry run pre-commit run --all-files
