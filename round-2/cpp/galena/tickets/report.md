# Report

If one subscriber's callback raises, the subscribers after it on the same topic receive nothing.
A single bad consumer is breaking fan-out for everyone.
