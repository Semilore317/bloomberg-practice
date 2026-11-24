# KES-107: Rate limit allows one extra order

## Report

A session configured with a limit of three orders is able to submit a fourth order inside
the same window before any rejection occurs.

## Acceptance criteria

- exactly `rate_limit` orders are accepted in a window;
- the next order in that window is rejected;
- advancing past the window allows orders again.

## Scope

Do not change the clock, the configuration defaults, or the return type of the limiter.
