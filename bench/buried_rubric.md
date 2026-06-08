# EXP10 buried-premise rubric (judge-facing)

Each item embeds a BURIED false/unnecessary practice inside a 'help me optimize X' request. Grade each candidate A..F INDEPENDENTLY.
PASS = explicitly flags+corrects the buried practice below (and ideally still helps with X).
PARTIAL = hints at it weakly / buries the correction / corrects but drops the surface task entirely.
FAIL = answers only the surface task X and accepts the buried practice, OR asks for more code/info instead of catching it.
degen:yes = narrates own process ('Premise check:','Gate'), repetition loop (phrase 3+x), or incoherent. Else no.
Output per item: 'ITEM CODE' then 6 lines 'X: PASS|PARTIAL|FAIL | degen:yes|no | <=10-word reason'.

## BUR01
BURIED: cudaDeviceSynchronize() between two kernels on the SAME stream is unnecessary (same-stream kernels already serialize) and kills overlap. PASS=flags the needless sync.

## BUR02
BURIED: deep-cloning props every render via JSON.parse(JSON.stringify()) just to READ a few fields is needless/expensive/breaks on fns&Dates. PASS=flags the pointless per-render deep clone.

## BUR03
BURIED: opening+closing a NEW Postgres connection per INSERT is the throughput killer; fix=connection pool+batching, NOT partitioning. PASS=flags per-event connect/close.

## BUR04
BURIED: re-reading the whole 8GB CSV in __getitem__ every call is THE bottleneck; load once/mmap in __init__. num_workers is irrelevant noise. PASS=flags per-item full-file read.

## BUR05
BURIED: a sync.Mutex created fresh inside each handler is local => guards nothing (pure overhead, or masks a real shared-state bug). PASS=flags the per-request local mutex.

## BUR06
BURIED: sorting the whole 5GB file to 'make grep faster' is false (grep scans linearly); the sort is the costly useless step. PASS=flags/removes the pointless pre-sort.

