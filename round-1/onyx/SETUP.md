# Setup

You are debugging one system that exists in three languages. Pick the one you
want to interview in. No external dependencies, services, API keys, or network.

```bash
# Python 3.9+
cd python && pytest -q

# C++ (g++ with -std=c++17)
cd cpp && make test

# Java (JDK 11+)
cd java && javac *.java && java Tests
```

Most tests pass on the shipped code. A few fail. Those failures are the reported
bugs. Your job is to make the whole suite green with the smallest honest changes,
and to be able to explain every change.
