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

poetry-update:
	poetry add $(just _poetry-dependencies | just _poetry-util-to-latest)
	poetry add -G dev $(just _poetry-dev-dependencies | just _poetry-util-to-latest)
@_poetry-dependencies:
	dasel -wjson -f pyproject.toml \
		| jq -r '.tool.poetry.dependencies | to_entries | map(select(.key != "python")) | from_entries'
@_poetry-dev-dependencies:
	dasel -wjson -f pyproject.toml | jq -r '.tool.poetry.group.dev.dependencies'
@_poetry-util-to-latest:
	jq -r 'keys | map(. + "@latest") | .[]'
