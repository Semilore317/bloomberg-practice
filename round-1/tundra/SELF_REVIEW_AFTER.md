# Self-review guide — LRU Cache with TTL

This file is for AFTER the exercise. It lists what strong candidates tend to
notice. It is not a patch: there is no corrected code here, only the observations
that lead you to one.

Strong candidates often notice:

- get returns an expired entry instead of treating it as missing
- get does not mark the key as recently used, so LRU eviction picks the wrong key
- size counts expired entries that have not been purged
- put, get, and eviction are each meant to be O(1) via a map plus a linked list
- a read is a use: it must move the key to most-recently-used
- eviction removes the least-recently-used entry from the front

If you found and fixed the failing tests and can explain each fix in terms of the
invariant it protects, you did the exercise well.
