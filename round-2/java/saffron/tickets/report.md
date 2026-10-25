# Report

The session store grows without bound. `cleanup` does nothing, so expired sessions accumulate and
leak memory over time.
