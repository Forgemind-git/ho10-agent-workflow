# Connector: LinkedIn / Twitter Posting Connector

## What This Connector Does

Takes a drafted post (from the Brand Voice Writer skill) and publishes it to LinkedIn and/or Twitter/X. Returns the live post URL and post ID so the workflow can log and notify.

## Supported Platforms

| Platform | API | Auth Method | Rate Limit |
|----------|-----|------------|------------|
| LinkedIn | LinkedIn API v2 | OAuth 2.0 (3-legged) | 100 posts/day |
| Twitter/X | Twitter API v2 | OAuth 2.0 + Bearer token | 17 posts/24h (free tier) |

---

## LinkedIn Setup

### Step 1 — Create a LinkedIn App

1. Go to https://developer.linkedin.com/
2. Click **Create App**
3. Fill in: App Name, LinkedIn Page (your company page), App Logo
4. Under **Products**, request access to: **Share on LinkedIn** and **Sign In with LinkedIn using OpenID Connect**
5. Note your **Client ID** and **Client Secret**

### Step 2 — Get an OAuth2 Access Token

LinkedIn uses a 3-legged OAuth flow. For automation, use the refresh token flow:

```bash
# 1. Get authorization URL (run once, open in browser)
curl "https://www.linkedin.com/oauth/v2/authorization?response_type=code&client_id=YOUR_CLIENT_ID&redirect_uri=https://your-redirect.com/callback&scope=w_member_social%20openid%20profile"

# 2. After approving, exchange the code for tokens
curl -X POST https://www.linkedin.com/oauth/v2/accessToken \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "grant_type=authorization_code&code=AUTH_CODE&redirect_uri=https://your-redirect.com/callback&client_id=YOUR_CLIENT_ID&client_secret=YOUR_CLIENT_SECRET"
```

### Step 3 — Post to LinkedIn

```bash
# Get your LinkedIn Member URN (run once)
curl -H "Authorization: Bearer ACCESS_TOKEN" https://api.linkedin.com/v2/me

# Create a post (text only)
curl -X POST https://api.linkedin.com/v2/ugcPosts \
  -H "Authorization: Bearer ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "author": "urn:li:person:YOUR_PERSON_ID",
    "lifecycleState": "PUBLISHED",
    "specificContent": {
      "com.linkedin.ugc.ShareContent": {
        "shareCommentary": {
          "text": "Your post text here"
        },
        "shareMediaCategory": "NONE"
      }
    },
    "visibility": {
      "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
    }
  }'
```

---

## Twitter/X Setup

### Step 1 — Create a Twitter Developer App

1. Go to https://developer.twitter.com/
2. Apply for a developer account (free tier is sufficient)
3. Create a Project and App
4. Under **User authentication settings**, enable OAuth 2.0
5. Set App permissions to **Read and Write**
6. Note your **Client ID** and **Client Secret**

### Step 2 — Get Access Token

```bash
# Twitter OAuth 2.0 PKCE flow for user context
# Use a library like tweepy or twitter-api-v2 for Python

pip install tweepy

python3 << 'EOF'
import tweepy

client = tweepy.Client(
    consumer_key="YOUR_API_KEY",
    consumer_secret="YOUR_API_SECRET",
    access_token="YOUR_ACCESS_TOKEN",
    access_token_secret="YOUR_ACCESS_TOKEN_SECRET"
)

# Test authentication
me = client.get_me()
print(f"Authenticated as: {me.data.username}")
EOF
```

### Step 3 — Post a Tweet

```python
import tweepy

def post_tweet(text: str, api_key: str, api_secret: str, access_token: str, access_token_secret: str) -> dict:
    client = tweepy.Client(
        consumer_key=api_key,
        consumer_secret=api_secret,
        access_token=access_token,
        access_token_secret=access_token_secret
    )
    response = client.create_tweet(text=text)
    tweet_id = response.data["id"]
    return {
        "success": True,
        "post_id": tweet_id,
        "post_url": f"https://twitter.com/i/web/status/{tweet_id}",
        "platform": "twitter"
    }
```

---

## Environment Variables

Add these to your `.env` file:

```env
# LinkedIn
LINKEDIN_CLIENT_ID=your_client_id
LINKEDIN_CLIENT_SECRET=your_client_secret
LINKEDIN_ACCESS_TOKEN=your_access_token
LINKEDIN_PERSON_URN=urn:li:person:YOUR_ID

# Twitter/X
TWITTER_API_KEY=your_api_key
TWITTER_API_SECRET=your_api_secret
TWITTER_ACCESS_TOKEN=your_access_token
TWITTER_ACCESS_TOKEN_SECRET=your_access_token_secret
```

---

## Required Permissions

| Platform | Permission Scope | Why needed |
|----------|----------------|-----------|
| LinkedIn | `w_member_social` | Create posts on behalf of user |
| LinkedIn | `openid`, `profile` | Get member URN for post author field |
| Twitter/X | Read and Write | Post tweets on behalf of account |

---

## Error Handling

| Error | Cause | Fix |
|-------|-------|-----|
| 401 Unauthorized | Expired or invalid token | Refresh OAuth token |
| 422 Unprocessable | Post too long | Truncate to platform limit (LinkedIn: 3000, Twitter: 280) |
| 429 Too Many Requests | Rate limit hit | Wait and retry with exponential backoff |
| 403 Forbidden | Wrong permission scope | Re-authorize with correct scopes |

---

## Connector Output Schema

```json
{
  "success": true,
  "results": [
    {
      "platform": "linkedin",
      "post_url": "https://www.linkedin.com/posts/...",
      "post_id": "urn:li:share:7214853921057480705",
      "published_at": "2026-06-27T08:00:31Z"
    },
    {
      "platform": "twitter",
      "post_url": "https://twitter.com/i/web/status/1806629182847741953",
      "post_id": "1806629182847741953",
      "published_at": "2026-06-27T08:00:33Z"
    }
  ],
  "total_posted": 2
}
```
