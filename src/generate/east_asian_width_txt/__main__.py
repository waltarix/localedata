from os import environ

from generate.east_asian_width_txt import generate, generate_derived
from generate.util.cache import Cache

if environ.get('AS_DERIVED', None):
    generate_derived(Cache.eaw_ranges())
else:
    generate(Cache.eaw_ranges())
