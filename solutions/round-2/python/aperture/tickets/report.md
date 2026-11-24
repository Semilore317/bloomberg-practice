# Report

A failing job retries forever and never reaches the dead-letter list. `nack` does not advance the
attempt count, and the dead-letter threshold is off by one, so the limit is never hit.
