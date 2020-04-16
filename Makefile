test:
	python -m pytest --cov-config .coveragerc --cov=jovian_papermill

test-coverage:
	coverage html -i
	open "htmlcov/index.html"
