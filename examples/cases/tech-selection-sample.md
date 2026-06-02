<!-- Illustrative draft for `falsify review`. Errors are INTENTIONALLY planted.
     Expected: the Skeptic flags ~4 issues and returns HOLD. -->

# Database choice: Postgres vs MongoDB for the events service

## Recommendation
We should adopt MongoDB for the new events service.

## Reasoning

Our events are semi-structured JSON, so a document store is the natural fit.
In our load test MongoDB handled **3x more writes per second** than Postgres, so
it will scale better as we grow.

Postgres can't index inside JSON columns, which means querying event payloads
would require full table scans — a dealbreaker at our volume.

We expect ~2,000 writes/sec at launch and ~50,000/sec within a year. Since
MongoDB won the write benchmark, it comfortably covers both.

Operationally, the team already runs Postgres, but MongoDB is "easy to operate,"
so the switch is low-risk.

## Conclusion
MongoDB is the clear choice for every service going forward.
