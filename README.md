# Skills for Claude Code

Free skills for Claude Code, made by Yauhen Massalski ([yauhenm.com](https://yauhenm.com)).
Each skill has its own folder and its own README with exact steps.

## Start here

**What is a skill?** A skill is a folder with a text file called `SKILL.md`. It teaches Claude Code
how to do one job well. Claude loads the skill when your request matches it.

**What is Claude Code?** It is Anthropic's tool that lets Claude work on your computer.
You need it installed before any skill here works.

### The skills

| Skill | What it does | Needs | Folder |
|---|---|---|---|
| podcast-notes | Turns a podcast episode into detailed notes on one web page | Mac, ffmpeg, whisper.cpp | [podcast-notes](https://github.com/holl4ndtv/skills/tree/main/podcast-notes) |
| web-qc | Checks a live web page on desktop and phone before you say it is done | Node.js, Playwright | [web-qc](https://github.com/holl4ndtv/skills/tree/main/web-qc) |
| loop-spec | Plans a repeating AI job with a real stop rule and proof | Nothing extra | [loop-spec](https://github.com/holl4ndtv/skills/tree/main/loop-spec) |
| write-a-skill | Helps Claude write a new skill the right way (Matt Pocock's method plus my rules) | Nothing extra | [write-a-skill](https://github.com/holl4ndtv/skills/tree/main/write-a-skill) |

Skills I use that someone else made. I do not copy them. Use the original:

| Skill | What it does | Original |
|---|---|---|
| stop-slop | Removes typical AI writing habits from any text | [hardikpandya/stop-slop](https://github.com/hardikpandya/stop-slop) |
| last30days | Finds what people say about a topic in the last 30 days | [mvanhorn/last30days-skill](https://github.com/mvanhorn/last30days-skill) |
| grilling | Questions you hard on a plan until it holds up | [mattpocock/skills](https://github.com/mattpocock/skills) (`productivity/grilling`) |

## Install any skill

Every skill is a folder. To install it, copy the folder into `~/.claude/skills/`.
Read the README inside the skill's folder first. Some skills need extra tools.

### Step 1: get the files

If you have Git:

```bash
git clone https://github.com/holl4ndtv/skills.git ~/skills
```

No Git? On the GitHub page, click the green **Code** button, then **Download ZIP**.
Unzip it. On a Mac, move the unzipped folder to your home folder and rename it `skills`.
On Windows, move it to `C:\Users\<your name>\skills`.

### Step 2: copy one skill folder

Mac (Terminal app):

```bash
mkdir -p ~/.claude/skills
cp -R ~/skills/web-qc ~/.claude/skills/
```

Windows (PowerShell):

```powershell
New-Item -ItemType Directory -Force "$env:USERPROFILE\.claude\skills"
Copy-Item -Recurse "$HOME\skills\web-qc" "$env:USERPROFILE\.claude\skills\"
```

Replace `web-qc` with the skill you want.

### Step 3: restart Claude Code and test

Close Claude Code and open it again. Type the test phrase from the skill's README.

### Or ask Claude Code to do it

Open Claude Code and type:

> Install this skill from https://github.com/holl4ndtv/skills/tree/main/web-qc

Claude will fetch the folder and put it in `~/.claude/skills/`. Then read the skill's README for any extra tools.

## Learn more

Free lessons for each skill: [yauhenm.com/learn](https://yauhenm.com/learn)

## License

MIT for my own skills (see [LICENSE](LICENSE)). Work from other authors keeps its own license. See [CREDITS.md](CREDITS.md).
