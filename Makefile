test:
	python -m pytest --cov-config .coveragerc --cov=jovian_papermill

test-coverage: test
	coverage html -i
	open "htmlcov/index.html"

black:
	black jovian_papermill
