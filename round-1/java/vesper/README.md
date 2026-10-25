# vesper - Connection Pool

`ConnectionPool` is a fixed-capacity connection pool.

You are joining this codebase late, and something in it is wrong. Users report pools that grow past their capacity, connections released twice, and a closed pool that still hands out connections. Your job is
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

Write your own `Check.java` with a `main` method, then:

```bash
javac *.java && java Check
```