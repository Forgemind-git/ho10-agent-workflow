# Workflow: Content Creation Pipeline

## Overview

This workflow automates the full content creation cycle: from discovering what's trending in your industry to publishing a polished, on-brand post — without manual research or copy-editing.

**Trigger options:**
- Scheduled: run daily at 08:00 via cron or n8n
- Manual: call `/content-pipeline run --topic-count 3`
- Webhook: POST to `/webhook/content-pipeline` with optional `{"industry": "AI"}` body

**Duration:** ~30–60 seconds end-to-end

---

## ASCII Flow Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                    CONTENT CREATION PIPELINE                │
└─────────────────────────────────────────────────────────────┘

  [TRIGGER]
  Cron / Manual / Webhook
        │
        ▼
┌──────────────────┐
│  STEP 1: MCP     │  trend-research-mcp
│  Gather Trends   │  ─────────────────────────────────────────
│                  │  • Fetches Google Trends RSS (daily feed)
│  INPUT:          │  • Fetches HackerNews top stories API
│  industry tag    │  • Filters by relevance score > 0.7
│                  │  • Returns top 3 topics with:
│  OUTPUT:         │    - headline
│  topics[]        │    - summary (2–3 sentences)
│                  │    - trend_score (0–1)
└────────┬─────────┘    - source_url
         │
         │ topics[] JSON
         ▼
┌──────────────────┐
│  STEP 2: SKILL   │  brand-voice-writer skill
│  Draft Post      │  ─────────────────────────────────────────
│                  │  • Picks highest-scored topic
│  INPUT:          │  • Applies brand voice rules:
│  topic + brand   │    - Tone: confident, practical, no hype
│  voice rules     │    - Hook in first line
│                  │    - 3 key insight lines
│  OUTPUT:         │    - CTA at end
│  post_draft{}    │    - 3–5 hashtags
│                  │  • Formats for platform character limit
│                  │  • Generates 2 variants (A/B)
└────────┬─────────┘
         │
         │ post_draft{} JSON
         ▼
┌──────────────────┐
│  STEP 3:         │  social-posting connector
│  CONNECTOR       │  ─────────────────────────────────────────
│  Post Content    │  • Selects variant A (or B if A fails)
│                  │  • Authenticates with OAuth2 token
│  INPUT:          │  • Posts to LinkedIn and/or Twitter
│  post_draft{}    │  • Returns:
│                  │    - post_url
│  OUTPUT:         │    - post_id
│  post_result{}   │    - timestamp
│                  │    - platform
└────────┬─────────┘
         │
         ▼
  [RESULT]
  post_result{} logged + notification sent
  ✓ Post live at: https://linkedin.com/posts/...
```

---

## Step-by-Step Detail

### Step 1 — MCP: Gather Trending Topics

**Server:** `trend-research-mcp`
**Tool called:** `get_trending_topics`

```json
// Input to MCP tool
{
  "industry": "artificial intelligence",
  "max_results": 5,
  "min_relevance_score": 0.7,
  "sources": ["google_trends", "hackernews", "rss_feeds"]
}
```

```json
// Output from MCP tool
{
  "topics": [
    {
      "headline": "OpenAI releases new model with 10x reasoning capability",
      "summary": "The latest release shows dramatic improvements in multi-step reasoning tasks. Benchmarks show near-human performance on graduate-level math and science questions. Developers report 60% reduction in prompt engineering time.",
      "trend_score": 0.94,
      "source_url": "https://news.ycombinator.com/item?id=12345"
    },
    {
      "headline": "EU AI Act enforcement begins for high-risk systems",
      "summary": "Compliance deadlines now active for AI systems in healthcare, finance, and critical infrastructure. Companies face fines up to 3% of global revenue for violations.",
      "trend_score": 0.88,
      "source_url": "https://techcrunch.com/..."
    }
  ],
  "fetched_at": "2026-06-27T08:00:00Z"
}
```

---

### Step 2 — Skill: Draft the Post

**Skill:** `brand-voice-writer`
**Input:** highest-scored topic from Step 1

The skill applies your brand voice rules and produces:

```json
// Output from skill
{
  "variant_a": {
    "text": "Most companies are still treating AI as a productivity hack.\n\nThe ones winning in 2026 are treating it as infrastructure.\n\nHere's the difference:\n→ Productivity hack: AI answers your questions\n→ Infrastructure: AI runs your workflows while you sleep\n\nOpenAI's new model isn't just smarter. It's the foundation layer that makes this shift possible for any team.\n\nAre you building on it — or watching from the sidelines?\n\n#AI #FutureOfWork #BusinessStrategy #AITools #Productivity",
    "character_count": 442,
    "platform": "linkedin"
  },
  "variant_b": {
    "text": "The new OpenAI model changes one thing most people are missing:\n\nAI is now infrastructure, not a tool.\n\nTeams that see this will outpace those that don't — by a lot.\n\nWhat are you building on it?\n\n#AI #OpenAI #FutureOfWork",
    "character_count": 220,
    "platform": "twitter"
  },
  "topic_used": "OpenAI releases new model with 10x reasoning capability",
  "generated_at": "2026-06-27T08:00:12Z"
}
```

---

### Step 3 — Connector: Publish the Post

**Connector:** `social-posting-connector`
**Action:** POST to LinkedIn API + Twitter API v2

```json
// Input to connector
{
  "platform": "linkedin",
  "content": "Most companies are still treating AI as a productivity hack...",
  "schedule": "now"
}
```

```json
// Output from connector
{
  "success": true,
  "post_url": "https://www.linkedin.com/posts/forgemind-ai_ai-futureofw...",
  "post_id": "urn:li:share:7214853921057480705",
  "platform": "linkedin",
  "published_at": "2026-06-27T08:00:31Z"
}
```

---

## How to Trigger

### Option A — Cron (recommended for daily posts)
```bash
# Add to crontab
0 8 * * 1-5 cd /your/project && node run-workflow.js content-pipeline
```

### Option B — Manual CLI
```bash
node run-workflow.js content-pipeline --industry "fintech" --platforms "linkedin,twitter"
```

### Option C — Webhook
```bash
curl -X POST https://your-server.com/webhook/content-pipeline \
  -H "Content-Type: application/json" \
  -d '{"industry": "AI", "platforms": ["linkedin"]}'
```

---

## Successful Run Checklist

- [ ] MCP returns at least 1 topic with trend_score >= 0.7
- [ ] Skill produces variant_a with character_count <= platform limit
- [ ] Connector returns `success: true` and a valid `post_url`
- [ ] Notification sent to Slack/email with post URL
- [ ] Run logged to database with status = "published"

See `sample_run.txt` for a complete real-output log.
