# LOOP SPEC: <loop name>

Full template. Use it for loops that touch production, a client, money, a paid API or shared rules.
(Quick, low-risk loop? Answer the 3 must-haves in chat.)

## MUST-HAVES (blank = do not build)

### 1. Goal (one sentence, concrete done)
>

### 2. Stop: ENFORCED, not promised
- Max iterations: `___`  · Max time, whole loop: `___`  · Max time, one step: `___`  · Max spend or tokens: `___`
- Why this interval (and not a longer one)? `___`  · What number shows the job is worth keeping? `___`
- What ACTUALLY enforces each limit (counter, child-process timeout, budget check, lock file): `___`
- Success check (external, NOT the model saying "done"): `___`
- Circuit breaker (same result or no progress: halt): `___`
- Kill-switch (how a person stops it in one step, for example a `STOP.flag` file): `___`

### 3. Proof and trust boundary
- What proves each step worked: `___`
- Can the loop create or edit that proof? The answer must be NO. (Good: live HTTP check, fixed browser test, an ID returned by the other service, an existing test exit code, an append-only log. Bad: file exists, git diff alone, a test or report the loop wrote.)

## THEN (non-trivial loops)

### 4. Pattern (plain words)
> sequential / event-driven / make-and-check / run-score-write-lesson:

### 5. Which model does which step
- Does it read private mail, notes, calendar or messages? Y/N. If Y: where does that data go, and did the user agree? `___`
- Cheap, fast model (bulk, sort, draft, label): `___`
- Strong model (judgment, final text, hard cases): `___`
- Escalate when: `___`

### 6. Safe to run twice, and state
- Safe to run twice? `___`
- Where progress is saved (state file): `___`
- Lock that stops overlapping runs: `___`
- Saved log it reads before posting, sending or repeating a step: `___`

### 7. Where the result lands (not only the terminal)
> A file, a note, a dashboard, a draft queue:

### 8. Blast radius and gate
- Touches money, a client, a store, production or shared rules? Y/N. If Y: DRAFTS only.
- Human gate: `___`

### 9. Where it runs
> Which machine, at what hours, and what happens if the machine is asleep or off:

### 10. Skills, output format, quality gate (overnight or scheduled loops)
> `___`

### 11. Smallest first version
> One source or channel, dry-run, no write-back, measure before scaling:

---
### Pre-build checklist
- [ ] Goal is concrete
- [ ] Every stop limit has a NAMED enforcer (code, not promise), including a per-step timeout, plus a kill-switch
- [ ] Success check is external
- [ ] Proof cannot be faked (the loop cannot edit it)
- [ ] Safe to run twice, and state is saved
- [ ] Result lands where the user looks
- [ ] Interval is justified, and the value number is named
- [ ] Money or client work = drafts plus a human gate
- [ ] Not wrapping a job that already works
- [ ] Stop guard written into the loop
