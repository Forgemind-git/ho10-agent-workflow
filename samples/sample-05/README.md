# HO10 Sample 05 — Personal Morning Briefing Workflow

## What you'll build
A personal "chief of staff" that hands you a clear plan before your first coffee. One trigger **gathers** today's calendar, your important unread emails, and a couple of relevant headlines, **summarises** them into a single 200–300 word brief with a focus for the day, then **delivers** it to your inbox or as your first calendar event. You assemble it in Claude.ai with a Skill, a Connector, and an MCP.

## Use it with your Claude.ai subscription
No API key needed. Just your normal Claude.ai login (Pro or Team).

1. Open **Claude.ai** → **Skills** (`claude.ai/skills`). Click **New Skill**, name it `morning-brief`, and paste in the full text from **`skill.md`**. Save it. This teaches Claude how to write your brief.
2. Go to **Settings → Connectors** (`claude.ai/settings/connectors`) and turn on **Gmail** and **Google Calendar** (or **Outlook**). Click **Connect** and sign in once. (Easy version of `connector.md`.)
3. To gather everything in one shot you can add the inputs MCP: open **Claude Desktop** (`claude.ai/download`) and paste the entry from **`mcp-config.json`** into its config, then restart it. *(Optional — the Gmail and Calendar connectors above can supply the inputs on their own.)*
4. Start a new chat and paste **the example prompt** below. Claude gathers, summarises, and delivers your brief.

## The example prompt
Copy this into a new Claude chat:

```
You are my morning chief of staff. Do all three steps and show me each result:

1. GATHER: Pull today's inputs — my Google Calendar events for today, my 10 most important unread emails (skip newsletters and receipts), and 2 news headlines relevant to my work. Use the connectors/MCP available to you.
2. SUMMARISE: Use my morning-brief skill to write one briefing under 300 words with these sections: Schedule (meetings in time order), Emails Needing Action (mark each 🔴 urgent / 🟡 today / 🟢 whenever), News (max 2 items), and Focus of the Day (one sentence). Calm, direct tone — no hype.
3. DELIVER: Show me the brief. Once I say "send it", email it to me via my Gmail connector with the subject "Morning Brief — [today's date]".

Wait for my approval before sending.
```

## The three pieces

| Piece | Role | What it does |
|-------|------|-------------|
| MCP — Morning Inputs | Data gatherer | Pulls calendar, emails, and news |
| Skill — Morning Brief Summariser | Shaper | Writes a scannable 200–300 word brief (see `skill.md`) |
| Connector — Gmail / Calendar | Actor | Emails the brief or files it as a calendar event |

## Files in this sample

- `skill.md` — the Morning Brief Summariser skill (paste into Claude → Skills)
- `workflow.md` — the full flow with a diagram and step-by-step detail
- `connector.md` — how the email/calendar connector works (advanced/manual setup)
- `mcp-config.json` — the inputs MCP entry for Claude Desktop
- `sample_run.txt` — a real end-to-end run you can read through
- `index.html` — open in your browser for a clickable setup guide

## Make it your own
- Tell the Skill what "important" means to you (specific senders, projects, or keywords).
- Change delivery to a calendar event at 07:00 instead of an email.
- Add a "tomorrow prep" line that flags anything you need to get ready tonight.

## Optional — automate it with the API (advanced)
You do **not** need this for the course. `connector.md` and `mcp-config.json` show the fuller manual setup (Gmail/Calendar API keys, running the MCP server, a 06:45 schedule). Only worth it once you want the brief to arrive every morning with zero clicks.
