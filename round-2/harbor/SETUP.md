# Setup

This pack ships no tests, on purpose. Read the tickets, form a hypothesis about
what is wrong, and write your own tests to confirm it before you change anything.
The same service exists in Python, C++, and Java; pick one.

## Python 3.9+

Write test files named `test_*.py` under `python/` (a `conftest.py` is already
there so your imports resolve), then:

```bash
cd python && pytest -q
```

## C++ (g++ with -std=c++17)

The implementation is header-only. Write your own `test.cpp` that includes the
headers, then:

```bash
cd cpp && g++ -std=c++17 test.cpp -o test && ./test
```

## Java (JDK 11+)

Write your own `Check.java` with a `main` that exercises the classes, then:

```bash
cd java && javac *.java && java Check
```
