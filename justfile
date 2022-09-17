@_list:
	just -l

yapf:
	poetry run yapf --recursive -vv -i src tests

isort:
	poetry run isort src tests

test:
	poetry run pytest
@test-picked:
	poetry run pytest --picked --testmon
test-watch:
	watchexec -p --shell none -e py -w tests -w src -c --on-busy-update=do-nothing -- just test-picked

lint:
	poetry run pyright
