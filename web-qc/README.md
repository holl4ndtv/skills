# web-qc

## What it does

It checks a live web page before you call it done. Claude opens the real site at desktop, tablet and
phone width. It looks for cut-off text, sideways scrolling and broken buttons. It zooms in on buttons,
prices and forms. It presses the real controls. It ends with a short report and a verdict.

## What you need

| Tool | What it is for | Cost |
|---|---|---|
| Claude Code | Runs the skill | Needs a Claude plan or API credits |
| Node.js 18 or newer | Runs the Playwright tool | Free. Get it at https://nodejs.org |
| Playwright MCP | Lets Claude open a browser and take screenshots | Free |

"MCP" means a plug-in that gives Claude extra tools. Playwright is a tool that controls a browser.
The browser runs in the background with no window, so it does not take over your screen.

## Install

1. Install Node.js (the LTS version) from https://nodejs.org. Check it with:

   ```bash
   node --version
   ```

2. Add the Playwright tool to Claude Code. This is one line, the same on Mac and Windows:

   ```bash
   claude mcp add playwright -- npx @playwright/mcp@latest --headless
   ```

3. Copy the skill folder. If you cloned this repo to `~/skills`:

   Mac:

   ```bash
   mkdir -p ~/.claude/skills
   cp -R ~/skills/web-qc ~/.claude/skills/
   ```

   Windows (PowerShell):

   ```powershell
   New-Item -ItemType Directory -Force "$env:USERPROFILE\.claude\skills"
   Copy-Item -Recurse "$HOME\skills\web-qc" "$env:USERPROFILE\.claude\skills\"
   ```

4. Restart Claude Code. Type `/mcp` and check that `playwright` shows as connected.
   The first time Claude opens a page, Playwright may need to download a browser (a few hundred MB). Allow it.

## Test it

Open Claude Code and type:

> QC the page https://example.com

You should get a report with DESKTOP, TABLET and MOBILE parts, a list of buttons pressed, and a verdict.

## Notes

- Claude will ask before it sends a form or buys anything on a real site.
- For a form test, give Claude an email address you own. Claude then checks that the message arrived.
- On a phone-width check, Claude says if it only resized the window and did not emulate a phone.

## How I use it

I run it on every page after I deploy it, before I tell anyone it is live.

## Credits

Written by Yauhen Massalski. MIT license (see the LICENSE file in the root of this repo).
Uses the Playwright MCP from Microsoft (https://github.com/microsoft/playwright-mcp) as a separate tool.
