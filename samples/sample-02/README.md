# Sample 02 — Lead Enrichment & Outreach Workflow

**Problem:** Sales reps waste hours researching each lead before writing a cold email. The result is either generic outreach that gets ignored, or slow personalised research that only covers a handful of prospects per day.

**This workflow solves it** by composing three pieces:

| Piece | Role | What it does |
|-------|------|-------------|
| MCP — Company Enrichment | Data Gatherer | Pulls company data, recent news, tech stack, and hiring signals |
| Skill — Personalised Outreach Drafter | Shaper | Writes a cold email that references specific, real details about the company |
| Connector — CRM (HubSpot/Notion) | Actor | Logs the drafted email to the lead's CRM record and queues it for send |

## The Three Pieces

### MCP: Company Enrichment MCP
Connects to Clearbit, Apollo.io, or LinkedIn to enrich a lead with company size, revenue range, tech stack, recent news, and job postings. Returns structured enrichment data ready for the skill.

See `mcp-config.json` for the server config.

### Skill: Personalised Outreach Drafter
A Claude skill that reads enrichment data and writes a short, specific cold email that does NOT sound like a template. The email references one real signal (a recent hire, a product launch, a job posting) and ties it to the prospect's likely pain point.

See `skill.md` for the full skill definition.

### Connector: CRM (HubSpot / Notion) Connector
Logs the drafted email to the contact's record in HubSpot or Notion, tags the contact with "outreach-drafted", and optionally enqueues the email in a sending sequence.

See `connector.md` for setup instructions.

## Files in this Sample

```
sample-02/
├── README.md          ← this file
├── workflow.md        ← full step-by-step flow with ASCII diagram
├── skill.md           ← Claude skill definition for Personalised Outreach Drafter
├── connector.md       ← HubSpot/Notion connector setup guide
├── mcp-config.json    ← MCP server configuration snippet
└── sample_run.txt     ← complete log of one successful run
```

## Quick Start

1. Configure your enrichment MCP using `mcp-config.json`
2. Add the skill from `skill.md` to your Claude Code project
3. Set up the CRM connector from `connector.md`
4. Trigger with a lead's email or domain (see `workflow.md`)

## Expected Output

A personalised cold email draft logged to CRM within ~25 seconds, referencing a real signal from the lead's company, with subject line variants and a suggested follow-up date.
