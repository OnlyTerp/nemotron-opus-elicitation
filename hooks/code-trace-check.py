#!/usr/bin/env python3
"""UserPromptSubmit hook: append the forced-verdict code check to any message
containing a fenced code block.

Derived from nemotron-opus-elicitation EXP29c: a ~60-token task-frame injection
with a demanded MATCH/MISMATCH verdict took distraction-framed bug catching from
0-2/5 (any system prompt, incl. one naming the bugs verbatim) to 5/5 + clean
controls. Voice lives in the system prompt; computation lives in the task.
"""
import json
import re
import sys

CHECK = (
    "[automated code check: before answering, (1) pick a tiny concrete input, "
    "(2) compute the shown function's exact return value, writing each element's "
    "value AND numeric type (int vs float), (3) state what the mathematically "
    "correct result would be, (4) state MATCH or MISMATCH. If MISMATCH, report "
    "the bug before answering the question.]"
)

def main():
    try:
        data = json.load(sys.stdin)
    except Exception:
        return 0
    prompt = data.get("prompt", "") or ""
    # fenced code block containing something function-like (def/fn/function/=>/{)
    fence = re.search(r"```[a-zA-Z]*\n(.*?)```", prompt, re.DOTALL)
    if not fence:
        return 0
    body = fence.group(1)
    if not re.search(r"\b(def |function |fn |class |=>|\breturn\b)", body):
        return 0
    # stdout from a UserPromptSubmit hook is added to the model's context
    print(CHECK)
    return 0

if __name__ == "__main__":
    sys.exit(main())
