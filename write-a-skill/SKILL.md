---
name: write-a-skill
description: "Creates a new agent skill with the right structure and bundled resources: a short SKILL.md, a trigger-rich description, reference files and scripts. Use when the user says things like: 'create me a skill', 'write a skill', 'new skill for', 'turn this workflow into a skill', 'write it the Pocock way'."
---

# Writing Skills

Read [HOUSE-RULES.md](HOUSE-RULES.md) in this folder before you draft. It holds the rules that came
from real incidents. This file is the method. That file is the list of mistakes to avoid.

## Process

0. **Check for an existing skill first.** List the installed skills (`ls ~/.claude/skills/` and the
   project's `.claude/skills/`). Before you draft, say in your first reply which existing skill is
   closest (name it) and pick one: (a) it already does the job, so use it; (b) extend it, so the new
   text goes into that skill (long parts in its `references/` folder); (c) truly new, with one line on
   why no existing skill fits. Do not answer from memory. Look at the real list.

1. **Gather requirements.** Ask the user:
   - What task or domain does the skill cover?
   - What specific use cases should it handle?
   - Does it need executable scripts, or only instructions?
   - Are there reference materials to include?

2. **Draft the skill.** Create:
   - `SKILL.md` with concise instructions
   - Extra reference files once `SKILL.md` would pass about 100 lines
   - Utility scripts if a step is deterministic

3. **Review with the user.** Present the draft and ask:
   - Does this cover your use cases?
   - Is anything missing or unclear?
   - Should any section have more or less detail?

4. **Install** only after the user says yes: put the folder in `~/.claude/skills/<name>/` (for all
   projects) or `<project>/.claude/skills/<name>/` (for one project).

5. **Try it once** on a real request before you say it works.

## Skill Structure

```
skill-name/
├── SKILL.md           # Main instructions (required)
├── REFERENCE.md       # Detailed docs (if needed)
├── EXAMPLES.md        # Usage examples (if needed)
└── scripts/           # Utility scripts (if needed)
    └── helper.js
```

## SKILL.md Template

```md
---
name: skill-name
description: Brief description of capability. Use when [specific triggers].
---

# Skill Name

## Quick start

[Minimal working example]

## Workflows

[Step-by-step processes with checklists for complex tasks]

## Advanced features

[Link to separate files: See [REFERENCE.md](REFERENCE.md)]
```

## Description Requirements

The description (plus the optional `when_to_use` field) is what your agent reads to decide which
skill to load. It sits in the system prompt next to every other installed skill. Claude Code gives all
skill listings about 1% of the context window. When that is full, descriptions are dropped (least
used first) and only the name stays. So keep it short and put the trigger words early.
(Checked 2026-10-19: https://code.claude.com/docs/en/skills)

**Goal:** give your agent just enough to know:

1. What capability the skill provides
2. When and why to trigger it (specific keywords, contexts, file types)

**Format:**

- Max 1024 characters (the portable Agent Skills limit). Claude Code also cuts the description plus `when_to_use` at 1,536 characters per skill in its listing (same URL).
- Write in third person.
- First sentence: what it does.
- Second sentence: "Use when [specific triggers]". Use the exact phrases people really say.

**Good example:**

```
Extract text and tables from PDF files, fill forms, merge documents. Use when working with PDF files or when user mentions PDFs, forms, or document extraction.
```

**Bad example:**

```
Helps with documents.
```

The bad example gives your agent no way to tell this skill from other document skills.

## Who can invoke it (Claude Code frontmatter)

- Default: the user and Claude can both invoke it.
- `disable-model-invocation: true`: only the user can start it (`/name`). The description leaves Claude's context. Use it for skills with side effects (deploy, publish, spend).
- `user-invocable: false`: hidden from `/`. Only Claude loads it. Use it for background knowledge.
- Claude-only keys such as `context: fork` and `effort` are not portable to other agents. Leave them out of skills meant for other tools.
(Checked 2026-10-19: https://code.claude.com/docs/en/skills)

## When to Add Scripts

Add utility scripts when:

- The operation is deterministic (validation, formatting)
- The same code would be generated again and again
- Errors need explicit handling

Scripts save tokens and are more reliable than code written fresh each time.

## When to Split Files

Split into separate files when:

- `SKILL.md` passes 100 lines (a house rule; Claude Code's own advice is under 500 lines)
- The content has distinct domains (finance vs sales schemas)
- Advanced features are rarely needed

## Review Checklist

After drafting, check:

- [ ] The description includes triggers ("Use when...")
- [ ] `SKILL.md` is under 100 lines
- [ ] No time-sensitive info
- [ ] Consistent terminology
- [ ] Concrete examples included
- [ ] References are one level deep
- [ ] Closest existing skill named, and "extend or new" decided
- [ ] Every path and skill name in the text really exists (`ls` it)
- [ ] The rules in HOUSE-RULES.md are applied
