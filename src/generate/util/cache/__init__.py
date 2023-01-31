import pickle
from pathlib import Path
from typing import Callable, TypeVar

from chars import eaw_ranges, wcwidth9_tables
from chars.char_ranges import CharRanges
from chars.tables import ByteTables

T = TypeVar('T')

cache_dir = Path('.cache')
eaw_cache = cache_dir.joinpath('eaw.pickle')
wcwidth9_cache = cache_dir.joinpath('wcwidth9.pickle')


class Cache():

    @classmethod
    def prepare(cls) -> None:
        cache_dir.mkdir(exist_ok=True)

    @classmethod
    def eaw_ranges(cls) -> CharRanges:
        return cls._cache(eaw_cache, eaw_ranges)

    @classmethod
    def wcwidth9_tables(cls) -> ByteTables:
        return cls._cache(wcwidth9_cache, wcwidth9_tables)

    @classmethod
    def _cache(cls, path: Path, generator: Callable[[], T]) -> T:
        if path.is_file():
            return pickle.load(path.open(mode='rb'))
        ranges = generator()
        pickle.dump(ranges, path.open(mode='wb'))
        return ranges
