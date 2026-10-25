# marlin - Inventory Reservations

`InventoryService` reserves stock for a fulfilment system.

You are joining this codebase late, and something in it is wrong. Users report stock counts that drift, holds that ship after they should have expired, and releases that free the same units twice. Your job is
to find the bug or bugs behind that, fix them, and prove each fix with a test you
write yourself. This pack ships no tests.

## Scope

In scope:

- find and fix the defects behind the reported symptom;
- write your own tests to confirm each defect and each fix;
- keep all existing, correct behaviour working.

Out of scope:

- redesigning the component or changing its public API;
- adding features the brief did not ask for;
- performance work, unless a defect is itself a performance bug.

Time budget: about 35 minutes.




## Running tests

Write your own `test.cpp` that includes the header, then:

```bash
g++ -std=c++17 test.cpp -o test && ./test
```