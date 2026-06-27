# Sample 01 — Content Creation Pipeline

**Problem:** Creating consistent, on-brand social media content is time-consuming. You need to research what topics are trending, write posts that match your brand voice, and then publish — all without losing hours of manual work each day.

**This workflow solves it** by composing three pieces:

| Piece | Role | What it does |
|-------|------|-------------|
| MCP — Trend Research | Data Gatherer | Fetches trending topics from Google Trends RSS or Feedly |
| Skill — Brand Voice Writer | Shaper | Drafts a polished post in your exact brand voice |
| Connector — LinkedIn/Twitter | Actor | Posts the final content to your chosen social platform |

## The Three Pieces

### MCP: Trend Research MCP
Connects to Google Trends RSS and tech news RSS feeds to surface the top 5 trending topics relevant to your industry. Returns a ranked list with headlines and brief descriptions.

See `mcp-config.json` for the server config.

### Skill: Brand Voice Writer
A Claude skill that takes a trending topic and drafts a social media post in your brand voice. The skill understands your tone, style rules, hashtag strategy, and character limits.

See `skill.md` for the full skill definition.

### Connector: LinkedIn / Twitter Posting Connector
Sends the drafted post to LinkedIn (via LinkedIn API) or Twitter/X (via Twitter API v2). Handles authentication, scheduling, and returns the post URL on success.

See `connector.md` for setup instructions.

## Files in this Sample

```
sample-01/
├── README.md          ← this file
├── workflow.md        ← full step-by-step flow with ASCII diagram
├── skill.md           ← Claude skill definition for Brand Voice Writer
├── connector.md       ← LinkedIn/Twitter connector setup guide
├── mcp-config.json    ← MCP server configuration snippet
└── sample_run.txt     ← complete log of one successful run
```

## Quick Start

1. Configure your MCP server using `mcp-config.json`
2. Add the skill from `skill.md` to your Claude Code project
3. Set up the connector credentials from `connector.md`
4. Trigger the workflow (see `workflow.md` for trigger options)

## Expected Output

A published social media post within ~45 seconds, with a returned post URL and engagement-ready copy in your brand voice.
