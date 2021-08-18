@_list:
	just -l

yapf:
	poetry run yapf --recursive -vv -i src tests

isort:
	poetry run isort src tests

test:
	poetry run pytest
