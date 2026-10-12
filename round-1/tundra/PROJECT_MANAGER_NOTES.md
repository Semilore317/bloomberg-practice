# Project Manager Notes - LRU Cache with TTL

Do not read this until after your first pass.

These are the questions a strong candidate asks before and during the fix. The
interviewer is playing the project manager, so some answers are judgement calls,
not facts in the code.

- Should a read return an entry that has expired?
- Does a read count as a use for LRU ordering?
- Should size count entries that have expired but not been purged?
- Which entry is evicted first when capacity is exceeded?
- Is get expected to be O(1)?
- On a tie, is insertion order or access order the tiebreak?
