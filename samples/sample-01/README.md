# HO10 Sample 1 — Content Pipeline

## Your task

As a content marketer you juggle research, writing and publishing across three tools. Build a composed workflow where an MCP fetches sources, a Skill drafts, and Cowork publishes.

## What you will build

A composed workflow connecting: an MCP tool (data fetching) → a Skill (processing/drafting) → Cowork (review + output)

## Components

- MCP tool: `fetch_sources(topic)` → list of URLs + summaries
- Skill: `draft_article(brief)` → structured draft
- Cowork step: review + schedule for publishing

## Build order

1. Build and test the MCP server (see `mcp-server/`)
2. Create the Skill in claude.ai
3. Connect them in a Cowork session
4. Run the full workflow end-to-end

## Required

Claude Desktop (for MCP) + Claude.ai Pro/Team (for Skills + Cowork)
