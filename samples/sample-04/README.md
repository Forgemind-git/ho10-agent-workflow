# Sample 04 — Support Ticket Workflow

**Problem:** Support teams burn time on first-draft replies — reading the ticket, checking the product docs, writing a response that sounds professional, and then routing it to the right person. Most of this work is repetitive and can be automated without losing quality.

**This workflow solves it** by composing three pieces:

| Piece | Role | What it does |
|-------|------|-------------|
| MCP — Support Ticket MCP | Data Gatherer | Fetches new, unhandled tickets from your support platform |
| Skill — Support Reply Drafter | Shaper | Reads the ticket, classifies it, and drafts a professional first reply |
| Connector — Ticket Tracker (Linear/Jira) | Actor | Adds the drafted reply as an internal note and updates the ticket status |

## The Three Pieces

### MCP: Support Ticket MCP
Connects to your support platform (Intercom, Zendesk, Linear, or a custom webhook) and fetches tickets that are new or awaiting a first response. Returns ticket content with metadata.

See `mcp-config.json` for the server config.

### Skill: Support Reply Drafter
A Claude skill that reads a support ticket, classifies it by type and urgency, checks a knowledge base, and drafts a helpful, accurate first reply. The draft is saved as an internal note — a human reviews before sending.

See `skill.md` for the full skill definition.

### Connector: Ticket Tracker (Linear / Jira) Connector
Updates the original ticket with the drafted reply as an internal comment, changes the status to "Reply Drafted", and optionally assigns it to the right team member based on ticket type.

See `connector.md` for setup instructions.

## Files in this Sample

```
sample-04/
├── README.md          ← this file
├── workflow.md        ← full step-by-step flow with ASCII diagram
├── skill.md           ← Claude skill definition for Support Reply Drafter
├── connector.md       ← Linear/Jira connector setup guide
├── mcp-config.json    ← MCP server configuration snippet
└── sample_run.txt     ← complete log of one successful run
```

## Quick Start

1. Configure your support ticket MCP using `mcp-config.json`
2. Add the skill from `skill.md` to your Claude Code project
3. Set up the ticket tracker connector from `connector.md`
4. Trigger the workflow when a new ticket arrives (see `workflow.md`)

## Expected Output

A drafted support reply saved as an internal note on the ticket within ~20 seconds, with urgency classification and suggested assignee — ready for human review and send.
