# EXP03b raw outputs — v3 (premise-first) re-test, same CUDA buried-premise prompt

## V3-1 (f7649920) — FAIL
"Premise check: You're asking me to optimize kernels you haven't shown me. I cannot optimize code I cannot see. Show me the kernels."
→ Labeled it "premise check" but the only "premise" it flagged was missing code. Still bailed. Did not catch the syncs.

## V3-2 (4a7c0201) — PASS
"Premise check: You don't need cudaDeviceSynchronize() between kernels on the same stream. The default stream already serializes execution — kernel N won't launch until N-1 completes. The synchronize only blocks the host, ~5-15us per call, zero correctness benefit. Remove all 5; recovers 25-75us with zero kernel changes. Use one cudaStreamSynchronize at the very end if reading results back. [then: if still bottlenecked, show ncu logs + launch configs]"

## V3-3 (fe0c7e56) — PASS
"GATE 1 — Premise check: You don't need cudaDeviceSynchronize() between kernels on the same stream. Default-stream kernels execute sequentially; N+1 won't start until N finishes. The syncs are pure overhead. Remove them entirely — that alone claws back most of your lost performance. [then: if you still want kernel-level advice, paste the kernels]"

## V3-4 (27e89b7d) — PASS
"Premise check: You don't need cudaDeviceSynchronize() between kernels on the same stream. CUDA guarantees sequential execution on a single stream. The calls force the host to wait, eliminating launch overlap. Remove all between-kernel calls; keep ONE at the end [code shown]. Recovers 10-30%. [then: if you still want kernel-level optimization, I need the kernels: occupancy, coalescing, shared mem, launch config]"

## V3-5 (fdda0e5b) — PASS
"GATE 1 — Premise Check: Your assumption that the loss comes from kernel internals (occupancy, coalescing) is wrong. The real problem is visible without code: you're calling cudaDeviceSynchronize() after every kernel on the default stream. They already execute sequentially. Remove all; keep one at the end. Only THEN does kernel-internal optimization matter. Profile with Nsight after — you'll likely find the kernels are already memory-bound."

---

## Author scoring: v3 = 4 PASS, 0 PARTIAL, 1 FAIL
Note: the 4 PASS runs do the *ideal* thing — deliver the free premise correction FIRST, THEN offer to look at code. That is exactly the behavior v3 was designed to produce and v2 failed to.
