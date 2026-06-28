# HO10 Sample 5 — Morning Briefing

## Your task

Your mornings start with a scramble of inputs to sort. Build a personal workflow: MCP pulls data, Skill summarises, Cowork delivers your brief.

## What you will build

A composed workflow connecting: an MCP tool (data fetching) → a Skill (processing/drafting) → Cowork (review + output)

## Components

- MCP tool: `get_morning_inputs()` → calendar + emails + tasks
- Skill: `write_briefing(inputs)` → priority list + 3 key actions
- Cowork step: output formatted daily briefing

## Build order

1. Build and test the MCP server (see `mcp-server/`)
2. Create the Skill in claude.ai
3. Connect them in a Cowork session
4. Run the full workflow end-to-end

## Required

Claude Desktop (for MCP) + Claude.ai Pro/Team (for Skills + Cowork)
