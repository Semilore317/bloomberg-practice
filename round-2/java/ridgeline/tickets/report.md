# Report

Under load the cache is evicting the entry that was just inserted instead of the
least-recently-used one. Hot data is being thrown away while cold data survives.
