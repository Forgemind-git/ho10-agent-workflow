# HO10 Sample 02 — Lead Enrichment & Outreach Workflow

## What you'll build
A workflow that turns a raw lead — just a name and a company — into a ready-to-send, personalised cold email logged in your CRM. One trigger does three things: it **researches** the company, **writes** an email that references a real, specific signal (a recent hire, a launch, a funding round), and **logs** it to the contact's record. You build it inside Claude.ai with a Skill, a Connector, and an MCP.

## Use it with your Claude.ai subscription
No API key needed. Just your normal Claude.ai login (Pro or Team).

1. Open **Claude.ai** → **Skills** (`claude.ai/skills`). Click **New Skill**, name it `outreach-drafter`, and paste in the full text from **`skill.md`**. Save it. This is your cold-email playbook.
2. Go to **Settings → Connectors** (`claude.ai/settings/connectors`) and turn on your CRM connector — for example **HubSpot** or **Notion**. Click **Connect** and sign in once. (Easy version of `connector.md`.)
3. For company research, open **Claude Desktop** (`claude.ai/download`) and paste the entry from **`mcp-config.json`** into its config so Claude can enrich the lead. Restart Claude Desktop. *(Optional — you can also paste in what you already know about the company.)*
4. Start a new chat and paste **the example prompt** below. Claude researches, drafts, and logs — pausing for your OK before it writes to the CRM.

## The example prompt
Copy this into a new Claude chat (swap in a real lead):

```
You are running my lead outreach workflow. Do all three steps and show me each result:

1. ENRICH: Research the company "Acme Robotics" (acmerobotics.com). Use the enrichment MCP if available, otherwise gather what you can. I need: company size, what they do, and at least one recent signal (a hire, launch, funding, or job posting).
2. DRAFT: Use my outreach-drafter skill to write a cold email to their Head of Operations. Build the whole email around the single strongest signal you found. Our product: "an AI workflow tool that removes manual ops handoffs." Keep it under 100 words with one clear call to action.
3. LOG: Show me the email. Once I say "log it", save it to this contact's record in my connected HubSpot/Notion connector and tag them "outreach-drafted".

Wait for my approval before logging anything.
```

## The three pieces

| Piece | Role | What it does |
|-------|------|-------------|
| MCP — Company Enrichment | Data gatherer | Pulls company size, news, and hiring signals |
| Skill — Outreach Drafter | Shaper | Writes a specific, non-template cold email (see `skill.md`) |
| Connector — CRM (HubSpot / Notion) | Actor | Logs the draft to the lead's record |

## Files in this sample

- `skill.md` — the Outreach Drafter skill (paste into Claude → Skills)
- `workflow.md` — the full flow with a diagram and step-by-step detail
- `connector.md` — how the CRM connector works (advanced/manual setup)
- `mcp-config.json` — the enrichment MCP entry for Claude Desktop
- `sample_run.txt` — a real end-to-end run you can read through
- `index.html` — open in your browser for a clickable setup guide

## Make it your own
- Put your real product one-liner and ideal-customer profile into the Skill.
- Change the target role in the prompt (Head of RevOps, VP Sales, Founder) to match who you sell to.
- Add a follow-up: ask Claude to also draft a 3-day follow-up email and save it as a task.

## Optional — automate it with the API (advanced)
You do **not** need this for the course. `connector.md` and `mcp-config.json` show the fuller manual setup (enrichment API keys, CRM tokens, running the MCP server). Only worth it once you want to enrich a whole list of leads unattended.
