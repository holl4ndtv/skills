---
name: loop-spec
description: "Writes a clear plan for any repeating AI loop (goal, stop rule, proof) before building it. Use when the user says things like: 'can this be made in a loop', 'spec the loop', 'when does the loop stop', 'loop plan', 'run this every hour', 'keep trying until it works'."
---

# loop-spec

A loop with no stop that is really enforced leads to runaway cost and a made-up "done". A plan is
worth nothing unless the STOP and the PROOF become real code, not a promise. Write the spec first,
then the guard, then the loop.

## Flow

1. **Draft the spec in chat.** Use the 3 must-haves below. A quick, low-risk loop needs no file.
2. **Write the full template file** (`references/LOOP-SPEC-TEMPLATE.md`) only when the loop touches
   production, a client, money, a paid API or shared rules. Then it is a record you can audit.
3. **Write the stop guard** (code below) into the real loop. Do not leave it as prose.
4. Build the smallest version: one source, one channel. Dry-run it and watch the guard and the proof fire. Then add the output step and the human gate.

## The 3 must-haves (never skip)

1. **Goal.** One sentence. A concrete "done".
2. **Stop (enforced, not promised).** Name the real thing that stops the loop: a counter, a timeout, a
   budget check, a lock file. Cover ALL of these: max iterations, max time for the whole loop, max time for
   one step, max spend or tokens, a real success check, and a circuit breaker (stop when nothing changes).
   If you cannot name what enforces a limit, stop and ask the user.
3. **Proof and trust boundary.** What proves a step worked, from a system the loop cannot create or edit?
   - Good: a live HTTP check, a browser test from FIXED tests, an ID returned by the other service, the exit code of an existing test suite, an append-only run log.
   - Bad (easy to fake): "the file exists", `git diff` alone, tests the loop wrote itself, reports the loop wrote itself. No real proof, no loop.

## Then answer (for any non-trivial loop)

4. **Pattern, in plain words.** "Do a list of steps once" (sequential). "React to events as they arrive" (event-driven). "Make it, have a critic check it, send it back" (make and check). "Run, score yourself, write a lesson, the next run reads it" (learning loop).
5. **How often, and why.** For a timed job, say why this interval and not a longer one. If the work is queued for weeks, "hourly" is waste: run only when new work can exist, or when an event fires. Say what number from an outside system shows the job is worth keeping. With no proof of value, recommend removing the job and ask the user. Never remove it yourself.
6. **Which model does which step.** Use a cheap, fast model for bulk work (sort, draft, label). Use a stronger model for judgment, final text and hard cases. Escalate only for money, clients, legal questions or low confidence. If the loop reads private mail, notes or messages, say where that data goes and get the user's OK first.
7. **Safe to run twice, and where progress is saved.** Where is progress stored (for example `state.json`), so a re-run does not redo work or charge twice? Before any step that posts, sends or repeats research, the loop reads the saved log and skips what is done. What stops two runs from overlapping (a lock file)?
8. **Where the result lands.** A file, a note, a dashboard, a draft queue. A result that only prints in a terminal is lost.
9. **Blast radius and gate.** Does it touch money, a client, a store, production or shared rules? Then it makes DRAFTS only, and a human approves. Never auto-publish, auto-pay or auto-edit rules. Name the kill-switch (how the user stops it fast).
10. **Skills, format, quality gate.** For an overnight or scheduled loop, name the skills or tools it calls, the output format, and the quality check. A bare prompt gives poor output.

## Write this guard (tune the numbers)

Run each step as its own program, with a timeout. A plain `step()` call inside the loop is NOT enough:
if `step()` hangs, no check in the loop ever runs again, so the time limit never fires. A child
process with `timeout=` is killed by the operating system when time runs out. That is the real stop.

```python
import os, subprocess, sys, time

STEP_CMD = ["python3", "step.py"]   # one step, as its own program (a script, or `claude -p "..."`)
MAX_ITERS = 50
MAX_SECONDS = 900                   # whole loop
STEP_SECONDS = 120                  # one step; the child process is killed after this
MAX_SPEND = 0.0                     # 0.0 = the step must not call a paid API

def spent():
    # Replace with a real meter (read the provider's usage, or a counter file) if the step is paid.
    # Fail closed: if the step is paid and you have no meter, do not run the loop.
    return 0.0

def success_check(out):
    # EXTERNAL proof: HTTP status, test exit code, an ID from another system. Not the model's word.
    raise NotImplementedError

def stop(why):
    sys.exit(f"STOP: {why}")

start, last = time.time(), None
for n in range(1, MAX_ITERS + 1):
    if os.path.exists("STOP.flag"):
        stop("kill-switch file found")
    left = MAX_SECONDS - (time.time() - start)
    if left <= 0:
        stop("loop time limit")
    if spent() > MAX_SPEND:
        stop("budget")
    try:
        r = subprocess.run(STEP_CMD, capture_output=True, text=True,
                           timeout=min(STEP_SECONDS, left))
    except subprocess.TimeoutExpired:
        stop("a step ran too long and was killed")
    out = r.stdout
    if r.returncode == 0 and success_check(out):
        break
    if out == last:
        stop("stuck: same result twice")      # circuit breaker
    last = out
else:
    stop("max iterations")
```

What this guard does and does not do:
- It stops the loop at the iteration limit, the total time limit, the budget, a `STOP.flag` file, and a repeated result.
- It kills a stuck step after `STEP_SECONDS`. The timeout kills the step's own process. If the step starts other programs, those can keep running: if so, run the step inside a container or use `os.killpg` on a process group.
- The spend check only works if `spent()` reads a real meter.
- The kill-switch: create a file named `STOP.flag` in the loop's folder, and the loop halts before the next step.

## Hard nos (traps and over-engineering)

- No loop around a plain scheduled job that already works (sync, index, backup, token refresh). A boring script stays boring.
- No swarm of agents for solo work.
- No agent grading its own work. The proof must be external. For screenshot graders: fix concrete defects, stop after two clean independent passes, and report any disagreement.
- No loop that edits its own instructions, skills or hooks without a human accept step.
- No strong, expensive model on high-volume, low-stakes steps. That is how bills explode.
- Local is not free: heavy jobs heat the machine and drain a laptop battery. Run them when the machine is idle.

For production or money loops, copy and fill [LOOP-SPEC-TEMPLATE.md](references/LOOP-SPEC-TEMPLATE.md).
