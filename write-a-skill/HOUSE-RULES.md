# House Rules for every skill

These rules come from real mistakes. Apply them next to the method in `SKILL.md`.

## Step 0: dedup before you write a line

1. List the installed skills (`ls ~/.claude/skills/` and the project's `.claude/skills/`). If one already covers the job, extend it or replace it on purpose. When you replace one, name it in the description.
2. Look for the rules you already follow in this domain (your notes, past corrections, project docs). Put the matching ones into the skill in plain words.
3. Write the description's trigger phrases in the words you really say. Do not use generic keywords.

## Craft principles

- **Name the ONE load-bearing insight** and say "This is the skill." Everything else is mechanical.
- **Hard gates:** "Do not proceed to X until Y." Refusing is a feature. A debugging skill that refuses to guess without a way to reproduce the bug is better than one that guesses.
- **Ordered escalation lists** ("try in roughly this order"), not unordered options.
- **Hard vs soft dependencies.** If the skill is WRONG without a config or a tool, say so and point to the setup. If it is only fuzzier without it, degrade gracefully in plain words. Do not add setup pointers out of habit.
- **Description = trigger surface.** First sentence: the capability. Then "Use when..." with the exact phrases the user says.
- `SKILL.md` stays near 100 lines. Split references one level deep. Put anything deterministic in a script.

## Invariants (breaking any of these caused a real incident)

- **Outputs go to a named project folder.** Give absolute paths in replies. Never leave files meant to be kept in `/tmp` or on the Desktop.
- **Anything visual gets a render check.** Open it in a browser at phone width (about 390 px) and desktop width, LOOK at the screenshot, fix, shoot again. A clipped badge once shipped because nobody looked.
- **Paid API calls: state the cost BEFORE spending.** Use subscription or free runners first. A non-interactive session cannot answer a prompt, so build in a `--yes`-style flag and say so in the skill.
- **Client-facing or public output is a draft** until the user approves it. Use plain language, no internal jargon, no absolute claims, nothing unverified.
- **Never end the skill's flow in a waiting state.** Finish the task, or state the blocker as a plain fact. Do not end with "now you do X and tell me."
- **Short reports.** Answer first, then the file paths. No recap of what you just did.
- **Try it on real data once** before you say the skill exists. The first run always finds a gap.
