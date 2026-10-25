# Cobalt (Python) Solution

## Bugs fixed

1. **Available balance ignored active holds**  
   - Issue: `available()` returned the full balance without subtracting active holds, so `authorize()` could not properly prevent spending held funds.  
   - Fix: `available()` now returns `balance - _active_holds(account_id)`.  
   - Regression: `test_held_funds_are_not_spendable` ensures held funds are not spendable and `authorize()` raises when insufficient available funds.

2. **Capture allowed on non-HELD holds**  
   - Issue: `capture()` could be called after a hold was voided/captured, changing state incorrectly.  
   - Fix: `capture()` raises `ValueError("hold is not held")` unless `h.status == HoldStatus.HELD`.  
   - Regression: `test_capture_does_not_run_after_void` verifies capture after void does not move funds or change status inappropriately.

3. **Void allowed on already voided/captured holds**  
   - Issue: `void()` could be called multiple times or on terminal holds, re-voiding or corrupting state.  
   - Fix: `void()` raises `ValueError("hold is not held")` unless `h.status == HoldStatus.HELD`.  
   - Regression: `test_void_on_already_voided_hold_raises` verifies re-voiding raises and state remains unchanged.

## Notes
- Operations on non-HELD holds raise `ValueError` (by the above checks).
- Existing correct behavior (e.g., balance unchanged on void, funds moved on capture) is preserved.
