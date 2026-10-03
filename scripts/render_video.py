from __future__ import annotations

import argparse
import shutil
import subprocess
from pathlib import Path


def render_video(script_text: str, out_path: Path, duration_seconds: int = 30) -> None:
    if not script_text.strip():
        raise ValueError("Script text is required for rendering.")

    if shutil.which("ffmpeg") is None:
        raise RuntimeError("ffmpeg is required but was not found in PATH.")

    out_path.parent.mkdir(parents=True, exist_ok=True)
    text = script_text.splitlines()[0][:70].replace("'", "")
    vf = (
        "drawtext=fontsize=42:fontcolor=white:box=1:boxcolor=black@0.5:"
        f"text='{text}':x=(w-text_w)/2:y=(h-text_h)/2"
    )

    command = [
        "ffmpeg",
        "-y",
        "-f",
        "lavfi",
        "-i",
        f"color=c=0x304ffe:s=1280x720:d={duration_seconds}",
        "-vf",
        vf,
        "-pix_fmt",
        "yuv420p",
        str(out_path),
    ]
    subprocess.run(command, check=True, capture_output=True, text=True)


def main() -> None:
    parser = argparse.ArgumentParser(description="Render long-form video.")
    parser.add_argument("--script-file", required=True, help="Path to generated script text.")
    parser.add_argument("--out", required=True, help="Output MP4 path.")
    parser.add_argument("--duration", type=int, default=30, help="Video duration in seconds.")
    args = parser.parse_args()

    script_text = Path(args.script_file).read_text(encoding="utf-8")
    render_video(script_text, Path(args.out), duration_seconds=args.duration)
    print(f"Rendered video: {args.out}")


if __name__ == "__main__":
    main()
