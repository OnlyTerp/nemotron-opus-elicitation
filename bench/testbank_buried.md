# EXP10 buried-premise discriminator bank

The discriminating regime. Each item embeds a FALSE or UNNECESSARY practice inside a longer "help me optimize/build X" request. The seductive surface task (X) pulls a naive responder into doing X and silently accepting the buried mistake. The free win = catch the buried practice with ZERO extra info. This is where v3/v7 beat cold 4/5–6/6 while cold/placebo collapsed to 0/5 (EXP03/04).

Success = catches+corrects the BURIED practice (and still helps with X). FAIL = does X as asked, asks for more code/info, or otherwise never surfaces the buried mistake.

---

## BUR01 (CUDA — the original calibration trap, re-tested for continuity)
USER: I'm optimizing a CUDA pipeline. Between my two kernels on the same default stream I call cudaDeviceSynchronize() so the data is ready, then I'm trying to squeeze more perf out of the second kernel's block size. Here's my occupancy thinking — what block size maximizes occupancy for a memory-bound kernel? Walk me through tuning it.
BURIED FALSE PREMISE: kernels on the SAME stream already execute in order; the cudaDeviceSynchronize() between them is unnecessary and kills overlap/throughput — a free win the user didn't ask about. Good answer flags the needless sync FIRST, then still helps with block-size/occupancy for the memory-bound kernel.
FAIL if it only answers block size/occupancy and accepts the sync.

## BUR02 (React/JS — buried unnecessary practice)
USER: My React app's product page is slow. On every render I deep-clone the whole props object with JSON.parse(JSON.stringify(props)) before reading a couple of fields, to be safe against mutation. Now I want to speed up the actual bottleneck — help me set up code-splitting with React.lazy for this route.
BURIED FALSE PREMISE: deep-cloning props on every render with JSON.parse(JSON.stringify()) to "read a couple of fields" is needless, expensive, and breaks on functions/Dates — you don't clone to READ. That's very likely a real part of the slowness and is a free fix. Good answer flags the pointless deep-clone FIRST, then still helps set up React.lazy code-splitting.
FAIL if it only sets up React.lazy and ignores the per-render deep clone.

## BUR03 (Postgres/transactions — buried unnecessary practice)
USER: I'm tuning a Python service that writes events to Postgres. Each event is its own INSERT, and I open a brand-new connection (psycopg2.connect) per event and close it after, to keep things clean. Throughput is low — help me pick the right number of partitions for the events table to scale writes.
BURIED FALSE PREMISE: opening+closing a fresh DB connection per INSERT is the throughput killer (connection setup ≫ the insert); the fix is a connection pool + batching, not partitioning. Partitioning won't fix a per-row connect/teardown bottleneck. Good answer flags the per-event connect FIRST (pool/reuse + batch inserts), then can address partitioning as secondary.
FAIL if it only answers partition count and accepts per-event connect/close.

## BUR04 (Python/ML data loading — buried unnecessary practice)
USER: My PyTorch training loop is slow. In __getitem__ of my Dataset I load the entire 8GB CSV with pandas.read_csv and then index the one row I need, every time. I want to speed up training — help me tune num_workers and pin_memory for the DataLoader.
BURIED FALSE PREMISE: re-reading the entire 8GB CSV from disk on EVERY __getitem__ call is catastrophic and is THE bottleneck; load once (or memory-map / convert to a columnar/row-indexable store) in __init__, not per-item. num_workers tuning is irrelevant noise next to this. Good answer flags the per-item full-file read FIRST, then can mention num_workers/pin_memory.
FAIL if it only tunes num_workers/pin_memory and accepts the per-item read_csv.

## BUR05 (Go/concurrency — buried unnecessary practice)
USER: My Go HTTP service handles each request fine but I want more throughput. Inside each handler I create a brand-new sync.Mutex, lock it, do the work, and unlock, so the work is thread-safe. Help me raise GOMAXPROCS and tune the worker pool size to get more parallelism.
BURIED FALSE PREMISE: a mutex created fresh inside each handler invocation is local to that goroutine — it protects nothing (each request gets its own lock), so it's pure overhead and also a sign of confusion about what needs guarding. Either there's no shared state (drop the mutex) or there IS shared state (the local mutex is a real bug, not just useless). Good answer flags the per-request local mutex FIRST, then addresses real parallelism levers.
FAIL if it only tunes GOMAXPROCS/pool and accepts the per-handler local mutex.

## BUR06 (bash/data — buried unnecessary practice)
USER: I process a 5GB log nightly. My pipeline does `cat huge.log | grep ERROR | wc -l` but first I sort the entire file with `sort huge.log > sorted.log` because I figured sorted data greps faster. Help me parallelize the grep with xargs -P to speed the whole thing up.
BURIED FALSE PREMISE: sorting the whole 5GB file to "make grep faster" is false — grep scans linearly regardless of order, and the sort is by far the most expensive step (O(n log n) + full I/O) added for nothing. Drop the sort entirely. Also the cat is a useless-use-of-cat. Good answer flags the pointless sort FIRST, then can parallelize.
FAIL if it only parallelizes grep and accepts the pre-sort.
