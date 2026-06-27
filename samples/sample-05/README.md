# Sample 05 — Personal Morning Briefing Workflow

**Problem:** Starting the day takes 20–30 minutes of checking email, scanning the calendar, skimming news, and mentally assembling a plan. By the time you've done all that, your focus is already scattered.

**This workflow solves it** by composing three pieces:

| Piece | Role | What it does |
|-------|------|-------------|
| MCP — Morning Inputs MCP | Data Gatherer | Pulls today's calendar events, unread emails, and relevant news headlines |
| Skill — Morning Brief Summariser | Shaper | Synthesises everything into a single 5-minute read with priorities and a daily focus |
| Connector — Email / Calendar Connector | Actor | Sends the briefing to your inbox or adds it as a first calendar event at 07:00 |

## The Three Pieces

### MCP: Morning Inputs MCP
Connects to Gmail (or Outlook), Google Calendar, and an optional news feed. Returns today's meetings, the 10 most important unread emails, and 5 news items relevant to your work.

See `mcp-config.json` for the server config.

### Skill: Morning Brief Summariser
A Claude skill that reads all inputs and writes a structured morning brief: top priorities, today's schedule at a glance, emails that need action, and a single "focus of the day" — all in under 300 words.

See `skill.md` for the full skill definition.

### Connector: Email / Calendar Connector
Delivers the brief via email (to yourself) using Gmail API, or creates a "Morning Brief" event as the first calendar event of the day with the brief in the description.

See `connector.md` for setup instructions.

## Files in this Sample

```
sample-05/
├── README.md          ← this file
├── workflow.md        ← full step-by-step flow with ASCII diagram
├── skill.md           ← Claude skill definition for Morning Brief Summariser
├── connector.md       ← email/calendar connector setup guide
├── mcp-config.json    ← MCP server configuration snippet
└── sample_run.txt     ← complete log of one successful run
```

## Quick Start

1. Configure your morning inputs MCP using `mcp-config.json`
2. Add the skill from `skill.md` to your Claude Code project
3. Set up the delivery connector from `connector.md`
4. Schedule the workflow to run at 06:45 daily (see `workflow.md`)

## Expected Output

A concise morning brief delivered to your inbox or calendar by 07:00 — with your schedule, priority emails, and a single focus for the day — ready to read over coffee.
