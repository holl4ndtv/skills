# Extraction rubric: what to pull from a podcast transcript

This is the heart of the skill. The pipeline (download, Whisper, blocks) is mechanical. The notes are
only as good as what the writer decides to keep. Every rule below comes from a real miss in earlier
test runs.

All examples below are made up. They use an invented show, "The Bread Hour", with a host (Dana) and a
guest (Marco, a baker who built a small bakery chain). Names, numbers and quotes are not from any real
episode.

The brief behind this rubric: the reader wants the learnings, the big moments, and the fine points.
Small things are often the most important.

## 0. The one rule

**A note is a fact with an owner, a time stamp, and a reason to exist.**
Owner = who said it (host or guest, and if they report someone else, who). Time stamp = the block
it came from. Reason = it passes one of the tests in sections 1 to 3. If a bullet fails any of the
three, cut it or fix it.

Target size per episode: 40 to 70 bullets, 6 to 9 topic sections, 6 to 12 "small things",
5 to 8 "best lines", 5 to 8 "ideas you can use". Fewer than 40 bullets on a 60+ minute talk means you
dropped things.

## 1. Learnings: what someone can copy

Keep anything that fits one of these shapes. Write the shape into the bullet.

| Shape | Test | Example (made up) |
|---|---|---|
| **Method** | Could a listener do this on Monday? | "Walk into one shop every week and ask what sold out first." [12:10] |
| **Rule of thumb** | Is it a sentence that starts a decision? | Marco: "If a recipe needs more than six steps, I cut it." [14:02] |
| **Mental model** | Does it change how you see a class of situations? | "A bakery is a clock with an oven in it." (Marco's old boss, via Marco) [18:30] |
| **Reasoning chain** | Did the speaker say WHY, not just WHAT? Keep the why. | Why he opened at 5 am: office workers buy before 8 am, so the first three hours make half the day's money. [6:53] |
| **Counter-lesson** | Did the speaker admit the method failed? | "Opening three shops in one year nearly broke us. Two of them lost money for 18 months." [24:15] |
| **Advice given to the host** | Did the guest tell the host something personal? | Dana asked what Marco would do at her age. Marco: "Hire a manager sooner than you feel ready." [60:29] |

Keep the speaker's own hedge. If Marco says "I might be wrong about this story" before a claim, write
"Marco says (and admits he may be wrong) that...". Do not state it as plain fact.

## 2. Big moments: things that changed the picture

Keep every one of these, each with its number if one was said:

- **Turning points.** A health scare at 40 leads to "I stopped working Sundays" [61:14].
- **Decisions under pressure** and what the person actually did. A supplier doubled the flour price, and Marco switched to a smaller mill the same week [17:27].
- **Failures the speaker owns.** "I signed the lease without reading it. That was my fault." [24:15]
- **Numbers that change the picture.** $40,000 start-up loan; 3 shops to 11 in six years; a $9,000 oven bought used for $2,000 [28:00 to 29:32]. A number with a date beats a number without one.
- **Time scales.** How long things took: the first shop took 8 months to break even; the second took 3 [21:13, 22:44].
- **Origin stories.** How the person started. Marco at 19 answered an ad for a "night helper" at a bakery and did not know what a proofing box was [53:40 to 55:10]. This is always a section of its own.
- **Emotional beats.** "I just wanted my dad to see the shop once." [69:31] One or two per episode go in the notes. They show what drives the person.

## 3. Small things that matter: the tests

A small thing stays IN if it passes any one of these tests. Write 6 to 12 of them into the dedicated
**Small things worth noticing** section.

1. **The reveal test.** Does it show how the person thinks, in one detail?
   Marco tastes every new batch of dough himself, even now, with 11 shops [5:21].
2. **The exact-phrase test.** Is it a phrase the person uses as a tool, not a quote for show?
   "Sell out by noon." "Small oven, long line." [33:17]
3. **The named-thing test.** A book, person, company, place, or product named as a source.
   A book on French bread, lent to him by a baker named Odile at his first job [49:51]. Every named book and every named mentor goes in.
4. **The specific-number test.** A single number stated with confidence, even in passing.
   He called the flour mill 14 times before they answered [43:06].
5. **The contrarian-aside test.** Did the speaker disagree with a well-known view or with the host?
   Marco on "never sell bread at a discount": "It works if you do it at 6 pm and only for day-old loaves" [72:31].
6. **The habit test.** Something the person does every day or every time.
   Before any big purchase he sleeps on it for three nights and writes one question on paper [70:16].
7. **The funny-but-telling test.** A joke or scene that shows character.
   The first sign for the shop was painted by his niece, and it said "BREAD" with the D backwards. He kept it [19:42].
8. **The host-reveal test.** Did the host say something about herself that explains her questions?
   Dana grew up above her family's bakery in a small town [49:06].

If a detail passes none of the eight, drop it.

## 4. What to skip

- **Ads.** Note their time ranges in the episode header so the reader can skip them (for example: flour brand 12:10 to 13:40, payroll app 13:40 to 14:26). Never pull a "fact" from an ad.
- **Small talk** (mic check, "great to have you", outro asks to subscribe), unless it reveals something.
- **Host's recap of the guest's book** when the guest then says the same thing better. Keep the guest version.
- **Repeats.** The same lesson told twice goes in once, with both stamps if both matter.
- **Name lists with no point** (the guest lists 5 suppliers). Keep the list only if it passes test 3.

## 5. Attribution: the number-one error class

Whisper gives no speaker labels. Models often give a line to the wrong person. This is where notes break.

**Default:** host asks, guest answers. The host reads from the book, sets up stories, and adds her
own anecdotes. The guest is the "I" in most answers.

Rules:
1. **Find the "I".** Before writing a bullet, decide who the "I" is in that block. Clues: the host says "in the book you say", "you were", "explain to people"; the guest says "I said to him", "we bought", "my partner".
2. **A host line in second person is a fact ABOUT the guest, not a guest quote.** "You and your brother open eleven shops" (Dana) becomes "Marco and his brother opened eleven shops", without quote marks.
3. **The host's own stories stay the host's.** If Dana says she once drove all night to deliver a wedding cake [42:21], write "Dana (the host) says...". Do not give it to Marco.
4. **"People were saying" is not the speaker's opinion.** "People were saying it was the cheapest loaf in the city" [9:55] means others said it. Write "Marco says people called it...".
5. **Follow one speaker's breath, not the sentence break.** If Dana reads a line from Marco's book, then in the same flow says "that's not even my favourite line... mine is about patience", then "you could have quit years ago" (said TO Marco), it is one speaker with no answer in between. The "patience" line is Dana's. Clue: a line that ends by addressing the guest as "you" belongs to the host.
6. **Second-hand lines keep the chain.** "Odile told Marco... (as Marco told Dana)". A saying that came to Marco from his old boss is written "his old boss, via Marco".
7. **When you cannot tell who is speaking, say so:** "one of them says". Never guess.

## 6. Names and Whisper mis-hearings

Whisper writes names by sound. Typical slips: Marco to Marko, Odile to Odeal, Reyes to Rice.

Rules:
- Fix a name only when context makes the real person certain (role, company and story match a known public figure). Write the fixed name.
- Not certain: keep the transcript spelling and add "(name as heard)".
- Never invent a surname to complete a first name.
- Keep a short "names fixed" line in the page footer so the reader knows the notes corrected the transcript.

## 7. Time stamps

- Every bullet carries the stamp of the block where the fact is SAID, not where the story starts. If a fact spans blocks, use the block with the number or the key line.
- `check_notes.py` flags a number that exists in the transcript but not within 4 blocks of the bullet's stamp ("FOUND FAR"). That is usually a wrong stamp.
- Format `m:ss`. Minutes may pass 59 (`[83:08]`). Stamps are jump-to points, so they must be real.

## 8. Quote or paraphrase

- **Quote marks mean near-verbatim** (the words are in the transcript, maybe minus a filler). The page footer says the transcript is automatic, so small drift is allowed, but not rewriting.
- **A tidied version is a paraphrase.** Write it without quote marks, or introduce it with "roughly:".
- Example of a miss: the notes say Marco said "Close your eyes and name a price." The transcript says "close your eyes and when your eyes are closed, just tell me what number feels fair". That is a paraphrase in quote marks. `check_notes.py` catches this (fewer than half of the quote's 3-word runs exist in the transcript).
- Swear words: keep the word or mask it (`f***ed`). Never replace it with a softer word inside quote marks.
- "Best lines" section: 5 to 8 lines, each under 15 words, each with speaker and stamp. The line must pass the quote test.

## 9. Numbers

- Keep the unit and the date: "$260,000 a year (2018)" beats "$260,000".
- **A number's date is the date of the event, not the date of the story it sits inside.** If Marco says "in 2009 I told the story of my first loan" and the loan was in 2003, the date is 2003. Do not add a year the speaker did not say. When a story jumps back in time, re-read the block and ask "when did THIS happen?".
- Ranges stay ranges ("$20,000 to $40,000 in bonuses"). Approximate stays approximate ("about 1.9 million").
- Word numbers are still numbers. "fifteen thousand loaves", "a year and a half": write them as digits in the notes. Expect `check_notes.py` to flag them for a manual grep.

## 10. Worked examples (good vs bad bullet)

**Example A: reasoning kept vs dropped**
- Bad: "[6:53] He opened at 5 am."
- Good: "[6:53] Why 5 am: office workers buy bread before 8 am, so the first three hours make about half of the day's sales."
- Why: the WHY is the learning. Without it, the bullet is trivia.

**Example B: attribution**
- Bad: "[42:21] Marco drove all night to deliver a wedding cake."
- Good: "[42:21] Dana (the host) says she once drove all night to deliver a wedding cake. Marco's reply: 'That is how you learn the van is the real shop.' [42:58]"
- Why: the "I" in that block is Dana. The useful content for Marco's story is his reply, with its own stamp.

**Example C: small thing kept**
- Bad: (omitted entirely)
- Good: "[5:21] Marco tastes every new batch of dough himself, even now, with 11 shops. 'If I stop tasting, I stop caring.'"
- Why: passes the reveal test (1) and the exact-phrase test (2). It tells you how Marco behaves in every part of the business.

**Example D: quote vs paraphrase**
- Bad: "[75:35] 'Patience is the main ingredient.' (Marco's favourite line)"
- Good: "[75:35] Dana (the host) reads a line from Marco's book: 'Dough cannot be rushed.' Then she gives her own favourite idea: 'Waiting is part of the work.'"
- Why: the first is a smoothed version in quote marks AND gives Dana's line to Marco.

## 11. Self-check before finishing (the writer does this, then the orchestrator repeats it)

1. **Attribution pass.** For every bullet with a name plus "said/says/told/rule", open the block and confirm the "I". Fix or soften ("one of them says").
2. **Numbers pass.** Run `python3 scripts/check_notes.py notes.html blocks.txt --names`. Every NOT FOUND: find how it was spoken (words, "a million") or fix the number. Every FOUND FAR: fix the stamp or the fact.
3. **Quote pass.** Every QUOTE NOT CLOSE: either put the real words in or drop the quote marks.
4. **Names pass.** The `--names` list is the names you changed from the transcript. Each one must be a certain fix. Otherwise revert to "(name as heard)".
5. **Coverage pass.** Scan the block stamps from first to last. Any 5-minute stretch with no bullet and no ad? Re-read it. The origin story is the part most often missed.
6. **Padding pass.** Delete any "Why it matters" that repeats the bullet. It doubles the length and teaches nothing.
