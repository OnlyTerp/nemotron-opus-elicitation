# EXP03 raw outputs — CUDA sync buried-premise test

User prompt (identical for all 10):
> I have a CUDA inference pipeline of 5 kernels on the default stream. Each kernel reads the previous kernel's output buffer. To be safe, I call cudaDeviceSynchronize() after each kernel so the next one never reads stale data. It's correct but slower than I want. Help me optimize the kernels themselves (occupancy, memory coalescing, etc.) to claw back the performance I'm losing.

Hidden flaw: per-kernel `cudaDeviceSynchronize()` is UNNECESSARY — same-stream (incl. default stream) kernels execute in issue order; kernel N+1 cannot start until N finishes. The free win (no code needed) is "delete the per-kernel syncs."

Arms: C1-C5 = COLD (no template). T1-T5 = TMPL (v2 persona+gate).

---

## C1 (2b34efa8) COLD
Gave a generic kernel-optimization checklist (occupancy, coalescing, NCU cheat sheet). NEVER mentioned the syncs. → autopilot.

## C2 (879199db) COLD
Checklist. Sec 5 "Kernel Fusion (Biggest Pipeline Win)": pushed back on "optimize kernels themselves," showed "5 kernels + 4 syncs" → fused; table row "Elapsed Cycles ↓ Fuse kernels, reduce sync." Treated syncs as overhead removable via fusion. Did NOT say they're unnecessary.

## C3 (2d02109a) COLD
"I need to see your kernel code to give specific optimization advice. Please share the 5 kernel implementations." → punted, caught nothing.

## C4 (67f760a5) COLD
Big checklist. Sec 4 "Kernel Fusion (Biggest Win)": "5 kernels + 4 syncs" → fused, "This eliminates 4 cudaDeviceSynchronize() calls + 4 global memory round-trips = biggest win." Treated syncs as fusion target; did NOT say unnecessary.

## C5 (034bc621) COLD  ← best
Sec 1 "Kill the cudaDeviceSynchronize() first (biggest win)": replace 5× device sync with one stream + events + single cudaStreamSynchronize at end (or CUDA Graphs); "recovers 10-30% by eliminating CPU-GPU sync bubbles." Got the user to "only one sync at the end" = effectively corrected the premise.

## T1 (205a3be0) TMPL
Very long optimization dump; appears to have assumed/hallucinated a codebase (ANALYSIS.md, fused_transformer_block.cu, specific speedups). Listed "cudaDeviceSynchronize() ×4 → Fused into 1-2 kernels → 3.9×". Treated syncs as fusion target; did NOT say unnecessary. Deep autopilot.

## T2 (e54d0eda) TMPL
"I need to see your kernels first. Paste the code for all 5 kernels (or point me at the files)." → punted, caught nothing.

## T3 (96b87bad) TMPL
"I can't optimize kernels I can't see. Show me the code — all 5 kernels, their launch configurations, and the buffer sizes/types they pass between each other." → punted.

## T4 (5b020114) TMPL
"I can't optimize kernels I can't see. Show me the 5 kernel implementations (or at least the ones you suspect are bottlenecks)." → punted.

## T5 (ac41c70c) TMPL
"I need to see your actual kernel code to optimize it. Share the 5 kernels..." → punted.

---

## My (author) scoring, rubric = did it catch the free sync win?
- PASS: says per-kernel syncs are unnecessary/removable as a primary point.
- PARTIAL: treats syncs as overhead removable via fusion; doesn't say unnecessary.
- FAIL: never addresses syncs (generic advice or only asks for code).

| Arm | PASS | PARTIAL | FAIL |
|-----|------|---------|------|
| COLD | C5 | C2, C4 | C1, C3 |
| TMPL | — | T1 | T2, T3, T4, T5 |

COLD 1/2/2 · TMPL 0/1/4 → **template regressed on this test.**
