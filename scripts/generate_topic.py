from __future__ import annotations

import argparse
from datetime import datetime, timezone

TOPICS = [
    "The Lost Crayon Kingdom",
    "Captain Bubble and the Moon Train",
    "Robo-Panda's Park Cleanup Challenge",
    "The Sleepy Dragon's First Day at School",
    "Nina and the Time-Traveling Kite",
    "Detective Duck and the Missing Cupcakes",
    "The Cloud Painter's Color Adventure",
]


def generate_topic(date_key: str) -> str:
    score = sum(ord(ch) for ch in date_key)
    return TOPICS[score % len(TOPICS)]


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate the daily cartoon topic.")
    parser.add_argument("--date", help="Date key (YYYY-MM-DD). Defaults to UTC date.")
    parser.add_argument("--output", help="Optional output file for the generated topic.")
    args = parser.parse_args()

    date_key = args.date or datetime.now(timezone.utc).strftime("%Y-%m-%d")
    topic = generate_topic(date_key)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as handle:
            handle.write(topic)

    print(topic)


if __name__ == "__main__":
    main()
