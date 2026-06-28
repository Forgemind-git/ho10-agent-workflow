# HO10 Sample 04 — Support Ticket Workflow

## What you'll build
A workflow that takes the grind out of first-draft support replies. One trigger **fetches** a new ticket, **drafts** a professional, accurate reply (and classifies how urgent it is), then **updates** your ticket tracker with the draft as an internal note for a human to review and send. Nothing goes to the customer without your OK. You build it in Claude.ai with a Skill, a Connector, and an MCP.

## Use it with your Claude.ai subscription
No API key needed. Just your normal Claude.ai login (Pro or Team).

1. Open **Claude.ai** → **Skills** (`claude.ai/skills`). Click **New Skill**, name it `support-reply-drafter`, and paste in the full text from **`skill.md`**. Save it. This is your reply-writing playbook.
2. Go to **Settings → Connectors** (`claude.ai/settings/connectors`) and turn on your ticket-tracker connector — for example **Linear** or **Jira**. Click **Connect** and sign in once. (Easy version of `connector.md`.)
3. For pulling tickets, open **Claude Desktop** (`claude.ai/download`) and paste the entry from **`mcp-config.json`** into its config. Restart Claude Desktop. *(Optional — you can also paste a ticket straight into the chat.)*
4. Start a new chat and paste **the example prompt** below. Claude classifies, drafts, and updates the tracker — leaving the reply as an internal note for review.

## The example prompt
Copy this into a new Claude chat (paste a real ticket in place of the example):

```
You are running my support workflow. Do all three steps and show me each result:

1. FETCH: Get the next unhandled ticket (use the support MCP if available; otherwise here is the ticket):
   Subject: "Charged twice after upgrading"
   Body: "I upgraded to Premium 5 days ago but still see the Free plan, and I've been billed twice. Please fix this today."
2. DRAFT: Use my support-reply-drafter skill. Classify the ticket type and urgency (P1–P4), suggest who should own it, and write a warm, specific first reply under 150 words that acknowledges the exact problem and gives a clear next step.
3. UPDATE: Show me the draft. Once I say "save it", add the reply as an internal note on the ticket via my connected Linear/Jira connector and set the status to "Reply Drafted".

Do not send anything to the customer. Wait for my approval before updating the tracker.
```

## The three pieces

| Piece | Role | What it does |
|-------|------|-------------|
| MCP — Support Ticket | Data gatherer | Fetches new, unanswered tickets |
| Skill — Support Reply Drafter | Shaper | Classifies and drafts a first reply (see `skill.md`) |
| Connector — Linear / Jira | Actor | Saves the draft as an internal note and updates status |

## Files in this sample

- `skill.md` — the Support Reply Drafter skill (paste into Claude → Skills)
- `workflow.md` — the full flow with a diagram and step-by-step detail
- `connector.md` — how the tracker connector works (advanced/manual setup)
- `mcp-config.json` — the support MCP entry for Claude Desktop
- `sample_run.txt` — a real end-to-end run you can read through
- `index.html` — open in your browser for a clickable setup guide

## Make it your own
- Paste your real FAQ or product docs into the Skill so replies cite accurate steps.
- Adjust the urgency rules (P1–P4) to match how your team triages.
- Add an "assign to" step that routes billing tickets to finance and bugs to engineering.

## Optional — automate it with the API (advanced)
You do **not** need this for the course. `connector.md` and `mcp-config.json` show the fuller manual setup (support-platform tokens, tracker API keys, running the MCP server). Only worth it once you want every new ticket pre-drafted automatically.
