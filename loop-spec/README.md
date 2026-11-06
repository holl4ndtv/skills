# loop-spec

## What it does

It helps you plan an AI loop before you build it. A loop is a job that repeats: "check this every hour"
or "keep trying until the test passes".

Claude writes down the goal, the stop rule and the proof of success. Then it writes a small stop guard
in Python. The guard ends the loop on a step limit, a time limit, a budget, a kill-switch file, or a
repeated result. It also kills one step that hangs.

## What you need

| Tool | What it is for | Cost |
|---|---|---|
| Claude Code | Runs the skill | Needs a Claude plan or API credits |
| python3 (to run the guard it writes) | Runs the stop guard | Free |

Nothing else. It works on Mac, Windows and Linux.

## Install

Mac or Linux. If you cloned this repo to `~/skills`:

```bash
mkdir -p ~/.claude/skills
cp -R ~/skills/loop-spec ~/.claude/skills/
```

Windows (PowerShell):

```powershell
New-Item -ItemType Directory -Force "$env:USERPROFILE\.claude\skills"
Copy-Item -Recurse "$HOME\skills\loop-spec" "$env:USERPROFILE\.claude\skills\"
```

Restart Claude Code.

## Test it

Open Claude Code and type:

> Spec the loop: every hour, check if my website is up, and stop when I say so.

You should get a goal, a stop rule with named limits, a proof check, and a stop guard in code.

## Notes

- The guard runs each step as its own program with a timeout. A step that hangs is killed after the time you set.
- If your step starts other programs, those can keep running after the kill. The skill explains how to handle that.
- The guard does not measure spend by itself. If your step uses a paid service, you must connect a real usage meter.

## How I use it

I run it before I build any job that repeats, so it cannot run forever or fake "done".

## Credits

Written by Yauhen Massalski. MIT license (see the LICENSE file in the root of this repo).
