from __future__ import annotations

import argparse
from pathlib import Path


def build_script(topic: str) -> str:
    clean_topic = topic.strip()
    if not clean_topic:
        raise ValueError("Topic cannot be empty.")

    return "\n".join(
        [
            f"Title: {clean_topic}",
            "Scene 1: Introduce the world and main character with upbeat music.",
            "Scene 2: Present a playful challenge with a funny twist.",
            "Scene 3: Resolve the challenge with teamwork and a positive moral.",
            "Narration style: family-friendly, energetic, and simple for all ages.",
        ]
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate the cartoon script.")
    parser.add_argument("--topic", help="Topic text for the script.")
    parser.add_argument("--topic-file", help="Path to a file containing topic text.")
    parser.add_argument("--output", required=True, help="Output path for script text.")
    args = parser.parse_args()

    topic = args.topic
    if not topic and args.topic_file:
        topic = Path(args.topic_file).read_text(encoding="utf-8").strip()

    if not topic:
        raise ValueError("Provide --topic or --topic-file with non-empty content.")

    script = build_script(topic)
    Path(args.output).write_text(script, encoding="utf-8")
    print(script)


if __name__ == "__main__":
    main()
