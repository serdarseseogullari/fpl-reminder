#!/usr/bin/env python3
"""
FPL Deadline Calendar Generator
Fetches gameweek deadlines from the FPL API and generates a subscribable .ics file.
Each event is placed 1 hour before the actual deadline, with a 30-minute duration.
"""

import requests
from datetime import timedelta
from zoneinfo import ZoneInfo
from icalendar import Calendar, Event, Alarm, vText, vDuration
from datetime import datetime
import uuid

FPL_API_URL = "https://fantasy.premierleague.com/api/bootstrap-static/"
OUTPUT_FILE = "calendar.ics"
LONDON_TZ = ZoneInfo("Europe/London")
OFFSET_BEFORE_DEADLINE = timedelta(hours=1)
EVENT_DURATION = timedelta(minutes=30)


def fetch_events():
    response = requests.get(FPL_API_URL, timeout=15)
    response.raise_for_status()
    data = response.json()
    return data["events"]


def build_calendar(fpl_events):
    cal = Calendar()
    cal.add("prodid", "-//FPL Deadline Calendar//fpl-calendar//EN")
    cal.add("version", "2.0")
    cal.add("calscale", "GREGORIAN")
    cal.add("method", "PUBLISH")
    cal.add("x-wr-calname", "FPL Deadlines")
    cal.add("x-wr-timezone", "Europe/London")
    cal.add("x-wr-caldesc", "Fantasy Premier League gameweek deadlines (1 hour early reminder)")
    cal.add("x-published-ttl", "PT6H")
    refresh = vDuration(timedelta(hours=6))
    refresh.params["VALUE"] = "DURATION"
    cal.add("refresh-interval", refresh)

    for fpl_event in fpl_events:
        gw_id = fpl_event["id"]
        gw_name = fpl_event["name"]  # e.g. "Gameweek 29"
        deadline_str = fpl_event["deadline_time"]  # e.g. "2026-03-03T18:00:00Z"

        # Parse deadline as UTC, convert to London time
        deadline_utc = datetime.fromisoformat(deadline_str.replace("Z", "+00:00"))
        deadline_london = deadline_utc.astimezone(LONDON_TZ)

        # Event starts 1 hour before deadline
        event_start = deadline_london - OFFSET_BEFORE_DEADLINE
        event_end = event_start + EVENT_DURATION

        summary = f"FPL {gw_name} Deadline"

        event = Event()
        event.add("uid", f"fpl-gw{gw_id}-deadline@fpl-calendar")
        event.add("summary", summary)
        event.add("dtstart", event_start)
        event.add("dtend", event_end)
        event.add("dtstamp", datetime.now(tz=LONDON_TZ))
        event.add(
            "description",
            f"FPL {gw_name} transfer deadline is in 1 hour. Make your transfers now!\n"
            f"https://fantasy.premierleague.com/"
        )
        event.add("url", "https://fantasy.premierleague.com/")

        # VALARM: notify at event start (i.e. 1h before deadline)
        alarm = Alarm()
        alarm.add("action", "DISPLAY")
        alarm.add("description", f"FPL {gw_name} deadline in 1 hour!")
        alarm.add("trigger", timedelta(0))  # trigger at event start
        event.add_component(alarm)

        cal.add_component(event)

    return cal


def main():
    print("Fetching FPL event data...")
    fpl_events = fetch_events()
    print(f"Found {len(fpl_events)} gameweeks.")

    print("Building calendar...")
    cal = build_calendar(fpl_events)

    print(f"Writing to {OUTPUT_FILE}...")
    with open(OUTPUT_FILE, "wb") as f:
        f.write(cal.to_ical())

    print("Done.")


if __name__ == "__main__":
    main()
