# Workflow: Daily Ops Data Pipeline

## Overview

This workflow runs every morning before the team arrives. It pulls the previous day's operational metrics, analyses them for anomalies, and delivers a formatted briefing to Slack — so the first thing the team sees each day is a prioritised list of what needs attention.

**Trigger options:**
- Scheduled: cron at 07:00 Monday–Friday
- Manual: `node run-workflow.js ops-pipeline --date 2026-06-27`
- Webhook: POST to `/webhook/ops-pipeline` with optional date override

**Duration:** ~30–45 seconds end-to-end

---

## ASCII Flow Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                    DAILY OPS DATA PIPELINE                      │
└─────────────────────────────────────────────────────────────────┘

  [TRIGGER]
  Cron 07:00 Mon–Fri / Manual
        │
        ▼
┌──────────────────┐
│  STEP 1: MCP     │  data-pull-mcp
│  Pull Metrics    │  ───────────────────────────────────────────
│                  │  • Queries configured data sources:
│  INPUT:          │    - PostgreSQL / MySQL
│  date, sources   │    - REST API endpoints
│                  │    - Google Sheets
│  OUTPUT:         │    - CSV/JSON files
│  metrics{}       │  • Fetches today + 7d + 30d baselines
│                  │  • Returns structured metrics object
└────────┬─────────┘
         │
         │ metrics{} JSON
         ▼
┌──────────────────┐
│  STEP 2: SKILL   │  ops-analyst skill
│  Analyse Data    │  ───────────────────────────────────────────
│                  │  • Compares each metric to baselines
│  INPUT:          │  • Calculates % deviation
│  metrics{}       │  • Classifies severity:
│                  │    🔴 CRITICAL: >20% deviation
│  OUTPUT:         │    🟡 WARNING: 10–20% deviation
│  analysis{}      │    🟢 NORMAL: <10% deviation
│                  │  • Writes plain-English summary
│                  │  • Suggests 1 action per anomaly
└────────┬─────────┘
         │
         │ analysis{} JSON
         ▼
┌──────────────────┐
│  STEP 3:         │  slack-connector
│  CONNECTOR       │  ───────────────────────────────────────────
│  Notify Slack    │  • Formats as Slack Block Kit message
│                  │  • Colour-codes by severity
│  INPUT:          │  • Posts to #ops-daily channel
│  analysis{}      │  • Pins message if CRITICAL anomalies exist
│                  │  • Returns Slack message permalink
│  OUTPUT:         │
│  slack_result{}  │
└────────┬─────────┘
         │
         ▼
  [RESULT]
  Slack message posted ✓
  Team can see anomalies before standup
```

---

## Step-by-Step Detail

### Step 1 — MCP: Pull Yesterday's Metrics

**Server:** `data-pull-mcp`
**Tool called:** `get_daily_metrics`

```json
// Input to MCP tool
{
  "date": "2026-06-26",
  "sources": [
    {
      "type": "postgres",
      "query": "SELECT COUNT(*) as orders, SUM(amount) as revenue FROM orders WHERE created_at::date = $1",
      "params": ["2026-06-26"],
      "metric_names": ["orders_count", "revenue_total"]
    },
    {
      "type": "api",
      "url": "https://your-api.com/metrics?date=2026-06-26",
      "auth_header": "Bearer ${API_KEY}",
      "extract_fields": ["support_tickets_opened", "avg_response_time_minutes"]
    }
  ],
  "include_baselines": true,
  "baseline_days": [7, 30]
}
```

```json
// Output from MCP tool
{
  "date": "2026-06-26",
  "metrics": {
    "orders_count": {
      "value": 143,
      "baseline_7d_avg": 187,
      "baseline_30d_avg": 172
    },
    "revenue_total": {
      "value": 28450,
      "baseline_7d_avg": 37200,
      "baseline_30d_avg": 34100
    },
    "support_tickets_opened": {
      "value": 47,
      "baseline_7d_avg": 28,
      "baseline_30d_avg": 31
    },
    "avg_response_time_minutes": {
      "value": 38,
      "baseline_7d_avg": 22,
      "baseline_30d_avg": 25
    }
  },
  "fetched_at": "2026-06-27T07:00:08Z"
}
```

---

### Step 2 — Skill: Analyse and Flag Anomalies

**Skill:** `ops-analyst`
**Input:** metrics from Step 1

```json
// Output from skill
{
  "date": "2026-06-26",
  "overall_status": "CRITICAL",
  "anomalies": [
    {
      "metric": "orders_count",
      "value": 143,
      "baseline_7d_avg": 187,
      "deviation_pct": -23.5,
      "severity": "CRITICAL",
      "plain_english": "Orders were 24% below the 7-day average. This is the lowest single-day count in the past 30 days.",
      "suggested_action": "Check checkout funnel for errors in the last 24h. Verify payment gateway uptime. Review any marketing campaign pauses."
    },
    {
      "metric": "revenue_total",
      "value": 28450,
      "baseline_7d_avg": 37200,
      "deviation_pct": -23.5,
      "severity": "CRITICAL",
      "plain_english": "Revenue was $8,750 below the 7-day average. Consistent with the order count drop — suggests a volume problem, not an AOV problem.",
      "suggested_action": "Cross-reference with orders anomaly. AOV ($199 vs avg $199) is normal — the drop is purely in volume."
    },
    {
      "metric": "support_tickets_opened",
      "value": 47,
      "baseline_7d_avg": 28,
      "deviation_pct": 67.9,
      "severity": "CRITICAL",
      "plain_english": "Support tickets spiked 68% above the 7-day average. This is likely connected to the order volume drop — customers experiencing issues.",
      "suggested_action": "Review ticket categories from yesterday. Check for a specific error type or product category driving the spike."
    },
    {
      "metric": "avg_response_time_minutes",
      "value": 38,
      "baseline_7d_avg": 22,
      "deviation_pct": 72.7,
      "severity": "CRITICAL",
      "plain_english": "Response time is 73% above normal. With 68% more tickets and 73% slower response, the support queue is severely stressed.",
      "suggested_action": "Assign additional support capacity immediately. Consider a status page update if the root issue is a product bug."
    }
  ],
  "normal_metrics": [],
  "executive_summary": "Yesterday (Jun 26) was a bad day across the board. Orders and revenue both dropped ~24% from weekly averages while support tickets spiked 68% with response times 73% above normal. The pattern suggests a product or checkout issue that affected both purchase conversion and customer experience simultaneously. Priority: identify root cause of checkout/order drop — the support spike will follow.",
  "recommended_priority": "Investigate checkout funnel and payment gateway first. Everything else likely cascades from there.",
  "analysis_generated_at": "2026-06-27T07:00:21Z"
}
```

---

### Step 3 — Connector: Post to Slack

**Connector:** `slack-connector`
**Action:** Post Block Kit message to #ops-daily

The Slack message looks like:

```
🔴 Daily Ops Briefing — Jun 26, 2026 | CRITICAL

4 anomalies detected | All metrics tracked: 4

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🔴 CRITICAL — orders_count
143 orders (↓24% vs 7d avg of 187)
Orders were 24% below the 7-day average — lowest in 30 days.
→ Check checkout funnel for errors in the last 24h

🔴 CRITICAL — revenue_total
$28,450 (↓24% vs 7d avg of $37,200)
Revenue $8,750 below average. AOV is normal — pure volume drop.
→ Cross-reference with orders anomaly

🔴 CRITICAL — support_tickets_opened
47 tickets (↑68% vs 7d avg of 28)
Support spiked 68% — likely connected to order drop.
→ Review ticket categories from yesterday

🔴 CRITICAL — avg_response_time_minutes
38 min (↑73% vs 7d avg of 22 min)
Queue is severely stressed with 73% slower responses.
→ Assign additional support capacity immediately
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Priority: Investigate checkout funnel first. Everything else cascades from there.
```

---

## How to Trigger

### Option A — Cron (recommended)
```bash
# Add to crontab (runs at 07:00 Mon-Fri)
0 7 * * 1-5 cd /your/project && node run-workflow.js ops-pipeline
```

### Option B — Manual with date override
```bash
node run-workflow.js ops-pipeline --date 2026-06-26
```

### Option C — Webhook
```bash
curl -X POST https://your-server.com/webhook/ops-pipeline \
  -H "Content-Type: application/json" \
  -d '{"date": "2026-06-26", "channel": "#ops-incidents"}'
```

---

## Configuration

Set anomaly thresholds in your `.env`:

```env
ANOMALY_CRITICAL_THRESHOLD=20   # % deviation = CRITICAL
ANOMALY_WARNING_THRESHOLD=10    # % deviation = WARNING
BASELINE_DAYS_PRIMARY=7         # Primary baseline (7-day avg)
BASELINE_DAYS_SECONDARY=30      # Secondary baseline (30-day avg)
```

## Successful Run Checklist

- [ ] MCP returns data for all configured metrics
- [ ] All baselines (7d, 30d) populated
- [ ] Skill identifies anomalies with severity ratings
- [ ] Slack message posted to correct channel
- [ ] Message pinned if any CRITICAL anomalies
- [ ] Run logged to database

See `sample_run.txt` for a complete real-output log.
