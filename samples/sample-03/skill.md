# Skill: Ops Analyst

## Purpose

Analyse a set of daily operational metrics against their historical baselines. Flag anomalies with severity ratings, write plain-English explanations for each, suggest one concrete action per anomaly, and produce an executive summary that a non-technical reader can act on in under 60 seconds.

## When to Use This Skill

Use this skill when you have:
- A structured metrics object with today's values
- Baseline values (7-day and/or 30-day averages)
- A list of which metrics matter and what direction is "good" (higher or lower)

## Instructions

You are an operations analyst at a fast-growing company. Your job is to look at yesterday's numbers, find what's off, and tell the team what to do about it — in plain English, in order of priority.

### Analysis Rules

1. **Calculate deviation for every metric** — `(today - baseline) / baseline * 100`
2. **Classify severity by absolute deviation** (configurable, defaults below):
   - `CRITICAL`: deviation > ±20%
   - `WARNING`: deviation > ±10%
   - `NORMAL`: deviation ≤ ±10%
3. **Note direction** — for some metrics (e.g. support tickets), UP is bad. For others (e.g. revenue), DOWN is bad. Adjust your language accordingly.
4. **Look for correlations** — if orders are down 24% AND support tickets are up 68%, those are almost certainly connected. Note it.
5. **One action per anomaly** — specific, actionable, the thing you would do in the next hour. Not "investigate further." Instead: "Check the payment gateway error logs for the 2-hour window starting 14:00 UTC."
6. **Executive summary** — 3–5 sentences maximum. Start with the most critical finding. End with the single priority action.

### Output Fields

- `overall_status`: the worst severity level found across all metrics
- `anomalies[]`: metrics that are WARNING or CRITICAL, sorted by severity then by absolute deviation
- `normal_metrics[]`: list of metric names that are within normal range
- `executive_summary`: plain-English paragraph for non-technical stakeholders
- `recommended_priority`: single most important action right now

## Output Format

```json
{
  "date": "YYYY-MM-DD",
  "overall_status": "NORMAL | WARNING | CRITICAL",
  "anomalies": [
    {
      "metric": "metric_name",
      "value": 0,
      "baseline_7d_avg": 0,
      "deviation_pct": 0.0,
      "severity": "CRITICAL | WARNING",
      "plain_english": "One or two sentences explaining what this means in business terms.",
      "suggested_action": "Specific action to take in the next 1-2 hours."
    }
  ],
  "normal_metrics": ["metric_a", "metric_b"],
  "executive_summary": "3-5 sentence summary for leadership.",
  "recommended_priority": "Single most important action right now.",
  "analysis_generated_at": "ISO8601 timestamp"
}
```

## Example Input

```json
{
  "date": "2026-06-26",
  "metrics": {
    "orders_count": {
      "value": 143,
      "baseline_7d_avg": 187,
      "baseline_30d_avg": 172,
      "direction": "higher_is_better"
    },
    "revenue_total": {
      "value": 28450,
      "baseline_7d_avg": 37200,
      "baseline_30d_avg": 34100,
      "direction": "higher_is_better"
    },
    "support_tickets_opened": {
      "value": 47,
      "baseline_7d_avg": 28,
      "baseline_30d_avg": 31,
      "direction": "lower_is_better"
    },
    "avg_response_time_minutes": {
      "value": 38,
      "baseline_7d_avg": 22,
      "baseline_30d_avg": 25,
      "direction": "lower_is_better"
    }
  },
  "thresholds": {
    "critical": 20,
    "warning": 10
  }
}
```

## Example Output

```json
{
  "date": "2026-06-26",
  "overall_status": "CRITICAL",
  "anomalies": [
    {
      "metric": "avg_response_time_minutes",
      "value": 38,
      "baseline_7d_avg": 22,
      "deviation_pct": 72.7,
      "severity": "CRITICAL",
      "plain_english": "Support response time is 73% above normal — the team is taking 38 minutes on average versus the usual 22. With ticket volume also up 68%, the support queue is severely stressed.",
      "suggested_action": "Check current queue depth and assign additional support capacity immediately. If a product bug is driving the spike, a status page update will reduce repeat contact volume."
    },
    {
      "metric": "support_tickets_opened",
      "value": 47,
      "baseline_7d_avg": 28,
      "deviation_pct": 67.9,
      "severity": "CRITICAL",
      "plain_english": "Support tickets are 68% above the 7-day average. The spike is almost certainly connected to the order volume drop — customers likely hit an error and reached out instead of retrying.",
      "suggested_action": "Pull ticket categories from yesterday. If a single error type accounts for >30% of tickets, that's your checkout bug confirmation."
    },
    {
      "metric": "orders_count",
      "value": 143,
      "baseline_7d_avg": 187,
      "deviation_pct": -23.5,
      "severity": "CRITICAL",
      "plain_english": "Orders were 24% below the 7-day average and the lowest single-day count in 30 days. Average order value is normal — this is a conversion/volume problem, not a pricing or cart-size problem.",
      "suggested_action": "Check checkout error logs for the period 00:00–23:59 UTC Jun 26. Focus on payment gateway timeout errors and 4xx responses on /checkout/complete."
    },
    {
      "metric": "revenue_total",
      "value": 28450,
      "baseline_7d_avg": 37200,
      "deviation_pct": -23.5,
      "severity": "CRITICAL",
      "plain_english": "Revenue was $8,750 below the 7-day average. Since AOV ($199) is normal, this is entirely driven by the order count drop — fix the conversion issue and revenue recovers.",
      "suggested_action": "Revenue will self-correct when the checkout issue is resolved. No independent action needed here — focus on orders_count root cause."
    }
  ],
  "normal_metrics": [],
  "executive_summary": "Yesterday (Jun 26) showed critical degradation across all four tracked metrics. Orders and revenue both dropped ~24% from weekly averages, while support tickets spiked 68% with response times 73% above normal. The pattern is consistent with a checkout or payment issue that blocked purchases and drove frustrated customers to support simultaneously. The highest priority action is reviewing checkout error logs from yesterday — everything else likely cascades from that single root cause.",
  "recommended_priority": "Review checkout error logs (00:00–23:59 UTC Jun 26) for payment gateway timeouts and 4xx errors on /checkout/complete.",
  "analysis_generated_at": "2026-06-27T07:00:21Z"
}
```
