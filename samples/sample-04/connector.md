# Connector: Ticket Tracker (Linear / Jira) Connector

## What This Connector Does

After the Support Reply Drafter skill produces a draft, this connector:
1. Finds the ticket in Linear or Jira by ticket ID
2. Adds the customer reply draft as an internal comment
3. Adds a separate internal note with the agent context
4. Updates ticket status to "reply-drafted"
5. Sets priority based on urgency (P1–P4)
6. Assigns to the suggested team member

## Supported Trackers

| Tracker | API | Auth Method |
|---------|-----|------------|
| Linear | GraphQL API | API Key |
| Jira | Jira REST API v3 | Basic Auth (email + API token) |
| Intercom | Intercom REST API | Bearer token |

---

## Linear Setup

### Step 1 — Get a Linear API Key

1. Go to Linear → Settings → API → Personal API Keys
2. Click **Create Key** → name it "Support Workflow"
3. Copy the key (shown only once)

### Step 2 — Find Your Team ID

```bash
curl -X POST https://api.linear.app/graphql \
  -H "Authorization: YOUR_LINEAR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"query": "{ teams { nodes { id name } } }"}'
```

### Step 3 — Add an Internal Comment

Linear uses GraphQL mutations:

```bash
# Add comment to issue
curl -X POST https://api.linear.app/graphql \
  -H "Authorization: YOUR_LINEAR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "mutation CommentCreate($input: CommentCreateInput!) { commentCreate(input: $input) { success comment { id url } } }",
    "variables": {
      "input": {
        "issueId": "ISSUE_ID_HERE",
        "body": "**DRAFT REPLY (do not send yet — review first)**\n\n---\n\nHi Rachel,\n\nThank you for reaching out...\n\n---\n\n**Internal note:** Known bug TECH-891. Admin export workaround available.",
        "createAsUser": "Support Workflow Bot",
        "displayIconUrl": "https://your-logo.com/bot-icon.png"
      }
    }
  }'
```

### Step 4 — Update Issue Status and Priority

```bash
# Update issue state (status) and priority
curl -X POST https://api.linear.app/graphql \
  -H "Authorization: YOUR_LINEAR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "mutation IssueUpdate($id: String!, $input: IssueUpdateInput!) { issueUpdate(id: $id, input: $input) { success issue { id title state { name } priority } } }",
    "variables": {
      "id": "ISSUE_ID_HERE",
      "input": {
        "stateId": "REPLY_DRAFTED_STATE_ID",
        "priority": 2,
        "assigneeId": "ASSIGNEE_USER_ID"
      }
    }
  }'
```

---

## Jira Setup (Alternative)

### Step 1 — Create an API Token

1. Go to https://id.atlassian.com/manage-profile/security/api-tokens
2. Click **Create API token**
3. Name it "Support Workflow"
4. Copy the token

### Step 2 — Add Internal Comment

```bash
curl -X POST "https://your-domain.atlassian.net/rest/api/3/issue/TICKET-4829/comment" \
  -H "Authorization: Basic $(echo -n 'you@email.com:YOUR_API_TOKEN' | base64)" \
  -H "Content-Type: application/json" \
  -d '{
    "body": {
      "type": "doc",
      "version": 1,
      "content": [{
        "type": "paragraph",
        "content": [{
          "type": "text",
          "text": "DRAFT REPLY (review before sending):\n\nHi Rachel,\nThank you for reaching out..."
        }]
      }]
    },
    "visibility": {
      "type": "role",
      "value": "Service Desk Team"
    }
  }'
```

### Step 3 — Update Ticket Status

```bash
# Get available transitions
curl "https://your-domain.atlassian.net/rest/api/3/issue/TICKET-4829/transitions" \
  -H "Authorization: Basic $(echo -n 'you@email.com:YOUR_API_TOKEN' | base64)"

# Apply a transition (e.g. move to "In Review")
curl -X POST "https://your-domain.atlassian.net/rest/api/3/issue/TICKET-4829/transitions" \
  -H "Authorization: Basic $(echo -n 'you@email.com:YOUR_API_TOKEN' | base64)" \
  -H "Content-Type: application/json" \
  -d '{"transition": {"id": "TRANSITION_ID_HERE"}}'
```

---

## Priority Mapping

The skill outputs P1–P4 urgency. Map to tracker priority:

| Skill Urgency | Linear Priority | Jira Priority |
|--------------|----------------|--------------|
| P1 | 1 (Urgent) | Highest |
| P2 | 2 (High) | High |
| P3 | 3 (Medium) | Medium |
| P4 | 4 (Low) | Low |

---

## Assignee Routing

Map skill's `suggested_assignee` to actual team member IDs:

```json
{
  "assignee_map": {
    "support-tier-1": "USER_ID_TIER1",
    "support-tier-2": "USER_ID_TIER2",
    "engineering": "USER_ID_ONCALL_ENG",
    "billing": "USER_ID_BILLING",
    "account-management": "USER_ID_CSM"
  }
}
```

---

## Environment Variables

```env
# Linear
LINEAR_API_KEY=lin_api_xxxxxxxxxxxxxxxxxxxx
LINEAR_TEAM_ID=your-team-id
LINEAR_REPLY_DRAFTED_STATE_ID=state-id-here

# Jira (alternative)
JIRA_DOMAIN=your-domain.atlassian.net
JIRA_EMAIL=you@yourcompany.com
JIRA_API_TOKEN=your-api-token
JIRA_PROJECT_KEY=TICKET

# Routing
ASSIGNEE_TIER1_ID=user-id-here
ASSIGNEE_TIER2_ID=user-id-here
NOTIFY_ASSIGNEE_SLACK=true
```

---

## Connector Output Schema

```json
{
  "success": true,
  "tracker": "linear",
  "ticket_id": "TICKET-4829",
  "ticket_url": "https://linear.app/yourteam/issue/TICKET-4829",
  "actions_taken": [
    "Status updated: open → reply-drafted",
    "Priority set: P2 (High)",
    "Internal comment added: draft reply (comment_id: abc123)",
    "Internal comment added: agent context (comment_id: abc124)",
    "Assigned to: support-tier-2 (@alex_support)",
    "Labels added: bug, data-export"
  ],
  "updated_at": "2026-06-27T14:23:22Z"
}
```
