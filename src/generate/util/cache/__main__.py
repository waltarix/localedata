from multiprocessing import Pool

from generate.util.cache import Cache

print('generate caches...')

Cache.prepare()

pool = Pool(processes=2)
results = [
    pool.apply_async(Cache.eaw_ranges),
    pool.apply_async(Cache.wcwidth9_tables),
]

[res.wait() for res in results]

print('done')
