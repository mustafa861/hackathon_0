# LinkedIn Auto-Posting

Automatically post business updates to LinkedIn to generate sales and engagement.

## How It Works

1. **Create a post** in `vault/Social_Posts/LinkedIn_Queue/`
2. **Run the poster**: `python src/linkedin_poster.py vault/ .linkedin_session/`
3. **Post is published** to LinkedIn automatically
4. **File moves** to `vault/Social_Posts/LinkedIn_Done/`

## Post Format

Create a markdown file in `vault/Social_Posts/LinkedIn_Queue/`:

```markdown
---
type: linkedin_post
status: draft
created: 2026-03-26
---

Your post content here...

Use emojis, hashtags, and formatting to make it engaging!

#YourHashtags #GoHere
```

## Example Post

See `vault/Social_Posts/Templates/example_post.md` for a template.

## Scheduling

To post automatically every day:

**Windows:**
```bash
schtasks /create /tn "AIEmployee_LinkedInPoster" /tr "python %CD%\src\linkedin_poster.py vault\ .linkedin_session\" /sc daily /st 09:00 /f
```

**Linux/Mac:**
```bash
# Add to crontab
0 9 * * * cd /path/to/project && python src/linkedin_poster.py vault/ .linkedin_session/
```

## Usage

### Manual Posting
```bash
python src/linkedin_poster.py vault/ .linkedin_session/
```

### With PM2 (Scheduled)
```bash
pm2 start src/linkedin_poster.py --name linkedin-poster --cron "0 9 * * *" -- vault/ .linkedin_session/
```

## Tips

- Post during business hours (9 AM - 5 PM) for better engagement
- Use relevant hashtags
- Include a call-to-action
- Add emojis for visual appeal
- Keep posts concise (under 300 words)

## Folder Structure

```
vault/Social_Posts/
├── LinkedIn_Queue/     # Place posts here to publish
├── LinkedIn_Done/      # Published posts move here
└── Templates/          # Example post templates
```
