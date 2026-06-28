# HO10 Sample 4 — Support Workflow

## Your task

Support replies are slow because fetching the ticket, drafting and updating the tracker are three separate jobs. Build a composed workflow.

## What you will build

A composed workflow connecting: an MCP tool (data fetching) → a Skill (processing/drafting) → Cowork (review + output)

## Components

- MCP tool: `get_ticket(id)` → ticket details + history
- Skill: `draft_reply(ticket)` → draft email + internal note
- Cowork step: update ticket status + send reply

## Build order

1. Build and test the MCP server (see `mcp-server/`)
2. Create the Skill in claude.ai
3. Connect them in a Cowork session
4. Run the full workflow end-to-end

## Required

Claude Desktop (for MCP) + Claude.ai Pro/Team (for Skills + Cowork)
