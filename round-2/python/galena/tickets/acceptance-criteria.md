# Acceptance criteria

- an exception in one callback does not stop delivery to the others;
- the handling of a failing callback is explicit rather than accidental;
- delivery to healthy subscribers still happens in order;
- add a test with one raising subscriber and one healthy subscriber that still receives the message.

Do not change topic matching or the subscription registry as part of this ticket.
