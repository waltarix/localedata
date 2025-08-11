export PYTHONPATH := 'src'

@_list:
	just -l

yapf:
	uv run yapf --recursive -vv -i src tests

isort:
	uv run isort src tests

test:
	uv run pytest
@test-picked:
	uv run pytest --picked --testmon
test-watch:
	watchexec -p --shell none -e py -w tests -w src -c --on-busy-update=do-nothing -- just test-picked

lint:
	uv run pyright

uv-update:
	# uv add $(just _uv-dependencies | just _uv-util-to-latest)
	uv add --dev -U $(just _uv-dev-dependencies | jq -r '.[]')
@_uv-dependencies:
	dasel -wjson -f pyproject.toml \
		| jq -r '.tool.uv["dependencies"] | map(split("[=<>]"; null) | first)'
# @_uv-dependencies:
# 	dasel -wjson -f pyproject.toml \
# 		| jq -r '.tool.uv["dev-dependencies"][]' | choose -f '[=<>]' 1 | jq -R add
@_uv-dev-dependencies:
	dasel -wjson -f pyproject.toml \
		| jq -r '.tool.uv["dev-dependencies"] | map(split("[=<>]"; null) | first)'
@_uv-util-to-latest:
	jq -r 'map(. + "@latest") | .[]'
