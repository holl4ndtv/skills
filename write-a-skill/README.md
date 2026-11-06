# write-a-skill

## What it does

It helps Claude write a new skill. It asks you what the skill should do, drafts a short `SKILL.md`,
writes a description that makes Claude pick the skill at the right time, and checks the result against a
list. It first checks that you do not already have a skill that does the job.

## What you need

| Tool | What it is for | Cost |
|---|---|---|
| Claude Code | Runs the skill | Needs a Claude plan or API credits |

Nothing else. It works on Mac, Windows and Linux.

## Install

Mac or Linux. If you cloned this repo to `~/skills`:

```bash
mkdir -p ~/.claude/skills
cp -R ~/skills/write-a-skill ~/.claude/skills/
```

Windows (PowerShell):

```powershell
New-Item -ItemType Directory -Force "$env:USERPROFILE\.claude\skills"
Copy-Item -Recurse "$HOME\skills\write-a-skill" "$env:USERPROFILE\.claude\skills\"
```

Restart Claude Code.

## Test it

Open Claude Code and type:

> Write a skill that checks my blog posts for spelling mistakes before I publish.

Claude should first name the closest skill you already have. Then it asks you a few questions and
drafts the skill.

## Credit and license

The method comes from Matt Pocock's skill-writing skill in https://github.com/mattpocock/skills.
His work is under the MIT license. His license text and copyright line are in the `LICENSE` file in
this folder. The license text was copied from his repo at commit `4ae2317`.

Note: in his repo at that commit the skill-writing guide lives under the name `writing-for-agents`.
The text in this folder is an adaptation of his earlier `write-a-skill` skill.

## Changed by Yauhen

- Added a first step: check the installed skills and pick "use it", "extend it" or "new".
- Added `HOUSE-RULES.md`: rules that came from real mistakes (outputs in named folders, a render check for anything visual, state the cost before spending, drafts for client and public work, no waiting state, short reports).
- Added notes on who can start a skill (`disable-model-invocation`, `user-invocable`) and the description length limits.
- Added a review checklist item for every path and skill name used in the text.
- Removed my private review and logging steps, because they only fit my own setup.

## How I use it

I use it each time I turn a repeated job into a skill.
