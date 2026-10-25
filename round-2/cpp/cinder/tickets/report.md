# Report

A delta for a symbol that has no prior snapshot silently fabricates a 0/0 base quote instead of
failing. Downstream consumers then see a bogus zero price. A delta only makes sense on top of a
snapshot.
