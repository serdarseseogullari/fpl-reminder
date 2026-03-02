# fpl-reminder

A subscribable calendar feed for Fantasy Premier League gameweek deadlines. Each event appears 1 hour before the actual deadline as a 30-minute reminder block, with a notification at the start. All 38 gameweeks included, with correct BST/GMT handling throughout the season.

## Overview

[Subscribe via GitHub Pages](https://serdarseseogullari.github.io/fpl-reminder) to add the feed to Google Calendar or Apple Calendar. Events update automatically — no manual re-importing needed.

## How it works

1. A GitHub Action runs every 6 hours and fetches the FPL bootstrap API
2. A Python script extracts the `deadline_time` for all 38 gameweeks and generates a `.ics` file
3. The file is committed to this repo and served via GitHub Pages
4. Subscribers receive updates automatically when deadlines change

## Tech Stack

- Python — `icalendar`, `requests`
- GitHub Actions — scheduled cron, auto-commits on change
- GitHub Pages — serves the `.ics` and landing page

## Local development

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python generate.py
```

Output: `calendar.ics`

## License

MIT
