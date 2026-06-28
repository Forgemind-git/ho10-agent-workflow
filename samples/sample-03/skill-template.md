# Skill Template — Ops Pipeline

## Purpose

TODO: Describe what this Skill does in 1–2 sentences.
This Skill is the analysis layer of the ops pipeline — it takes raw metrics and surfaces anomalies and a summary.

## When to use this Skill

TODO: Describe the trigger — when should Claude invoke this Skill?

## Inputs

| Input | Type | Description |
|-------|------|-------------|
| TODO  | TODO | TODO        |

## Output format

TODO: Describe the structure Claude should return.

## Instructions to Claude

```
TODO: Write the Skill prompt here.

Your Skill should:
1. Accept the output from the MCP fetch_ops_data tool
2. Analyse the metrics and flag any anomalies
3. Return a summary + anomaly list that the Cowork step can route to Slack or email

Remember to stay focused on the ops pipeline use case.
```

## Example

**Input:**
```
TODO: paste a sample input here
```

**Expected output:**
```
TODO: paste a sample output here
```
