# FPL Reminder

A subscribable calendar feed for Fantasy Premier League gameweek deadlines.

Each event is placed **1 hour before** the actual deadline as a 30-minute reminder block, with a notification at the start. All 38 gameweeks are included, with correct BST/GMT handling throughout the season.

**[Subscribe at serdarseseogullari.github.io/fpl-reminder](https://serdarseseogullari.github.io/fpl-reminder)**

---

## How it works

1. A GitHub Action runs every 6 hours and fetches the [FPL bootstrap API](https://fantasy.premierleague.com/api/bootstrap-static/)
2. A Python script extracts the `deadline_time` for all 38 gameweeks and generates a `.ics` file
3. The file is committed to this repo and served via GitHub Pages
4. Subscribers automatically receive updates when deadlines change

## Stack

- **Python** — `icalendar`, `requests`
- **GitHub Actions** — scheduled cron, auto-commits on change
- **GitHub Pages** — serves the `.ics` and landing page

## Local development

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python generate.py
```

Output: `calendar.ics`
