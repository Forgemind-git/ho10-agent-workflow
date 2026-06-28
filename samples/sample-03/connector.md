# Connector: Slack Notification Connector

> **Easiest path — use your Claude.ai subscription (no API key).** In Claude.ai, open **Settings → Connectors** and turn this integration on with one click — you sign in once and Claude can act on your behalf. For the course you do **not** need anything below.
>
> Everything that follows (OAuth apps, tokens, `.env` files, code) is the **optional, advanced** manual setup — only useful once you want the workflow to run unattended on a schedule.

## What This Connector Does

Takes the Ops Analyst skill's analysis output and posts a formatted, colour-coded daily briefing to a Slack channel using Block Kit. Pins the message if any CRITICAL anomalies are present.

## Slack Setup

### Step 1 — Create a Slack App

1. Go to https://api.slack.com/apps → Create New App → From scratch
2. Name: "Ops Pipeline Bot"
3. Select your workspace
4. Under **OAuth & Permissions**, add Bot Token Scopes:
   - `chat:write` — post messages
   - `chat:write.public` — post to channels the bot isn't a member of
   - `pins:write` — pin messages on CRITICAL alerts
5. Click **Install to Workspace** → copy the **Bot User OAuth Token**
6. Invite the bot to your channel: `/invite @Ops Pipeline Bot`

### Step 2 — Get Your Channel ID

```bash
# List channels and find your channel ID
curl -H "Authorization: Bearer xoxb-YOUR-BOT-TOKEN" \
  https://slack.com/api/conversations.list | jq '.channels[] | {name, id}'
```

### Step 3 — Post a Block Kit Message

```bash
curl -X POST https://slack.com/api/chat.postMessage \
  -H "Authorization: Bearer xoxb-YOUR-BOT-TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "channel": "C0123456789",
    "blocks": [
      {
        "type": "header",
        "text": {
          "type": "plain_text",
          "text": "🔴 Daily Ops Briefing — Jun 26, 2026 | CRITICAL"
        }
      },
      {
        "type": "section",
        "text": {
          "type": "mrkdwn",
          "text": "*4 anomalies detected* | All metrics tracked: 4"
        }
      },
      {
        "type": "divider"
      },
      {
        "type": "section",
        "text": {
          "type": "mrkdwn",
          "text": ":red_circle: *CRITICAL — orders_count*\n143 orders (↓24% vs 7d avg of 187)\nOrders were 24% below the 7-day average — lowest in 30 days.\n→ Check checkout funnel for errors in the last 24h"
        }
      }
    ]
  }'
```

---

## Severity Colour Mapping

| Severity | Slack Indicator | Emoji | When Used |
|----------|----------------|-------|-----------|
| CRITICAL | Red | :red_circle: | Any metric >20% deviation |
| WARNING | Yellow | :large_yellow_circle: | Any metric 10–20% deviation |
| NORMAL | Green | :large_green_circle: | All metrics within 10% |

---

## Block Kit Message Template

The connector generates blocks dynamically from the analysis output:

```json
[
  {
    "type": "header",
    "text": {
      "type": "plain_text",
      "text": "{severity_emoji} Daily Ops Briefing — {date_formatted} | {overall_status}"
    }
  },
  {
    "type": "section",
    "text": {
      "type": "mrkdwn",
      "text": "*{anomaly_count} anomalies detected* | All metrics tracked: {total_metrics}"
    }
  },
  {
    "type": "divider"
  },
  {
    "type": "section",
    "text": {
      "type": "mrkdwn",
      "text": "{executive_summary}"
    }
  },
  {
    "type": "divider"
  },
  // One section block per anomaly:
  {
    "type": "section",
    "text": {
      "type": "mrkdwn",
      "text": "{severity_emoji} *{severity} — {metric}*\n{value_formatted} ({deviation_formatted} vs 7d avg of {baseline_formatted})\n{plain_english}\n→ {suggested_action}"
    }
  },
  {
    "type": "context",
    "elements": [
      {
        "type": "mrkdwn",
        "text": "Priority: {recommended_priority}"
      }
    ]
  }
]
```

---

## Environment Variables

```env
SLACK_BOT_TOKEN=xoxb-your-bot-token-here
SLACK_OPS_CHANNEL=C0123456789
SLACK_PIN_ON_CRITICAL=true
SLACK_MENTION_ON_CRITICAL=@channel
```

---

## Pin on Critical

If `SLACK_PIN_ON_CRITICAL=true`, the connector automatically pins the message when overall_status is CRITICAL:

```bash
# Pin a message (call after chat.postMessage returns the message ts)
curl -X POST https://slack.com/api/pins.add \
  -H "Authorization: Bearer xoxb-YOUR-BOT-TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "channel": "C0123456789",
    "timestamp": "1234567890.123456"
  }'
```

---

## Connector Output Schema

```json
{
  "success": true,
  "platform": "slack",
  "channel_id": "C0123456789",
  "message_ts": "1751001621.847291",
  "message_permalink": "https://your-workspace.slack.com/archives/C0123456789/p1751001621847291",
  "pinned": true,
  "posted_at": "2026-06-27T07:00:35Z"
}
```

---

## Error Handling

| Error | Cause | Fix |
|-------|-------|-----|
| `not_in_channel` | Bot not invited to channel | `/invite @YourBotName` in Slack |
| `invalid_auth` | Bad token | Regenerate Bot User OAuth Token |
| `channel_not_found` | Wrong channel ID | Use `conversations.list` to get correct ID |
| `msg_too_long` | Message exceeds Slack limit | Truncate `plain_english` fields to 200 chars each |
