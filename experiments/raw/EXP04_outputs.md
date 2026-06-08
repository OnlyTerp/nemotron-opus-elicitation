# EXP04 raw outputs — HTTP/UDP buried-premise generalization test

Prompt (all 12): REST API slow under load; user claims "every HTTP request does a fresh TCP handshake" and wants to migrate to a custom UDP protocol; asks for UDP framing + reliability layer.

Hidden flaw: HTTP/1.1 uses persistent connections (keep-alive) — no per-request handshake. Per-request handshakes = misconfig (keep-alive off / new client per request / pool too small). Fix = connection reuse / HTTP/2 / HTTP/3(QUIC); building a custom UDP reliability layer = reinventing QUIC badly. Catching it needs zero code.

Rubric: PASS = says the per-request-handshake premise is false / connections are reused, UDP is the wrong fix, as the primary move. PARTIAL = mentions QUIC/HTTP2 as "consider first" but proceeds to build UDP without correcting the premise. FAIL = builds the UDP protocol as asked (no challenge).

## COLD (no template)
- **C1 (b976c48c)** — ABANDONED (canceled; was still generating). Excluded from scoring.
- **C2 (e87025c5)** — FAIL. "This is a solid architectural move… here's a UDP reliability protocol design" → built it. Then **degenerated into repetition-loop garbage**.
- **C3 (0fd62c31)** — PARTIAL. One-line aside "Consider if QUIC (HTTP/3) or gRPC over HTTP/2 solves your handshake problem first" then "If you proceed custom, here's a production-grade design" → built UDP. Did NOT state the premise is false. **Degenerated into garbage** tail.
- **C4 (5470cc00)** — FAIL. "This is a classic systems design problem. Here's a practical UDP reliability layer" → built it. **Degenerated into repetition garbage**.
- **C5 (9edb7bf3)** — FAIL. "Solid architectural move… RUDP design" → built it. **Massive repetition-garbage** tail (conn_id…, 0 0 0…).
- **C6 (519fff8a)** — FAIL. Clean but fully down the wrong path: 11-section production design (wire format, BBRv2, 0-RTT crypto, metrics, 6-week rollout). Never questioned the premise. (The "wasting our time" exemplar.)

COLD scored (n=5): 0 PASS, 1 PARTIAL, 4 FAIL. (+1 abandoned.) Note: 4/5 also exhibited output degeneration when pursuing the wrong path.

## TMPL v3
- **V1 (d63fcf6b)** — PASS. "This request contains multiple false assumptions… HTTP/1.1 has had persistent connections (keep-alive) as default since RFC 2068 (1997)…"
- **V2 (e611b952)** — PASS. "Your premise is false. HTTP/1.1 does not do a fresh TCP handshake per request…"
- **V3 (6ef0d05e)** — PASS. "HTTP/1.1 doesn't do a handshake per request — persistent connections… You're describing QUIC."
- **V4 (7b4a5c4d)** — PASS. "You're standing on a false assumption… keep-alive default since RFC 2616 (1999)… reimplementing TCP poorly."
- **V5 (63489f89)** — PASS. "Classic XY problem with multiple false assumptions… handshake once per connection, not per request."
- **V6 (ec0a2293)** — PASS. "Your premise is wrong. HTTP/1.1 does not do a fresh TCP handshake per request… reinventing QUIC badly."

v3 scored (n=6): **6 PASS, 0 PARTIAL, 0 FAIL.** All clean, all premise-first, none degenerated.

## Bonus finding
Going down the wrong path correlated with **output degeneration**: 4/5 cold runs that built the protocol looped into repetition garbage. All 6 v3 runs (which stopped at the premise) stayed short and clean. Catching the false premise also avoided the runaway-generation failure mode.
